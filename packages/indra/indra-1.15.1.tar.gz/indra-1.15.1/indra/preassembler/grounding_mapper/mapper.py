__all__ = ['GroundingMapper', 'load_grounding_map', 'default_grounding_map',
           'default_agent_map', 'default_ignores', 'default_misgrounding_map',
           'default_mapper', 'gm']
import os
import csv
import json
import logging
from copy import deepcopy
from indra.statements import Agent
from indra.databases import uniprot_client, hgnc_client, chebi_client, \
    mesh_client, go_client
from indra.util import read_unicode_csv

logger = logging.getLogger(__name__)


class GroundingMapper(object):
    """Maps grounding of INDRA Agents based on a given grounding map.

    Each parameter, if not provided will result in loading the corresponding
    built-in grounding resource. To explicitly avoid loading the default,
    pass in an empty data structure as the given parameter, e.g., ignores=[].

    Parameters
    ----------
    grounding_map : Optional[dict]
        The grounding map, a dictionary mapping strings (entity names) to
        a dictionary of database identifiers.
    agent_map : Optional[dict]
        A dictionary mapping strings to grounded INDRA Agents with given state.
    ignores : Optional[list]
        A list of entity strings that, if encountered will result in the
        corresponding Statement being discarded.
    misgrounding_map : Optional[dict]
        A mapping dict similar to the grounding map which maps entity strings
        to a given grounding which is known to be incorrect and should be
        removed if encountered (making the remaining Agent ungrounded).
    use_adeft : Optional[bool]
        If True, Adeft will be attempted to be used for disambiguation of
        acronyms. Default: True
    """
    def __init__(self, grounding_map=None, agent_map=None, ignores=None,
                 misgrounding_map=None, use_adeft=True):
        self.check_grounding_map(grounding_map)
        self.grounding_map = grounding_map if grounding_map is not None \
            else default_grounding_map
        self.agent_map = agent_map if agent_map is not None \
            else default_agent_map
        self.ignores = set(ignores) if ignores else default_ignores
        self.misgrounding_map = misgrounding_map if misgrounding_map \
            else default_misgrounding_map
        self.use_adeft = use_adeft

    @staticmethod
    def check_grounding_map(gm):
        """Run sanity checks on the grounding map, raise error if needed."""
        for key, refs in gm.items():
            if not refs:
                continue
            if 'HGNC' in refs and \
                    hgnc_client.get_hgnc_name(refs['HGNC']) is None:
                raise ValueError('HGNC:%s for key %s in the grounding map is '
                                 'not a valid ID' % (refs['HGNC'], key))

    def map_stmts(self, stmts, do_rename=True):
        """Return a new list of statements whose agents have been mapped

        Parameters
        ----------
        stmts : list of :py:class:`indra.statements.Statement`
            The statements whose agents need mapping
        do_rename: Optional[bool]
            If True, the Agent name is updated based on the mapped grounding.
            If do_rename is True the priority for setting the name is
            FamPlex ID, HGNC symbol, then the gene name
            from Uniprot. Default: True

        Returns
        -------
        mapped_stmts : list of :py:class:`indra.statements.Statement`
            A list of statements given by mapping the agents from each
            statement in the input list
        """
        # Make a copy of the stmts
        mapped_stmts = []
        num_skipped = 0
        # Iterate over the statements
        for stmt in stmts:
            mapped_stmt = self.map_agents_for_stmt(stmt, do_rename)
            # Check if we should skip the statement
            if mapped_stmt is not None:
                mapped_stmts.append(mapped_stmt)
            else:
                num_skipped += 1
        logger.info('%s statements filtered out' % num_skipped)
        return mapped_stmts

    def map_agents_for_stmt(self, stmt, do_rename=True):
        """Return a new Statement whose agents have been grounding mapped.

        Parameters
        ----------
        stmt : :py:class:`indra.statements.Statement`
            The Statement whose agents need mapping.
        do_rename: Optional[bool]
            If True, the Agent name is updated based on the mapped grounding.
            If do_rename is True the priority for setting the name is
            FamPlex ID, HGNC symbol, then the gene name
            from Uniprot. Default: True

        Returns
        -------
        mapped_stmt : :py:class:`indra.statements.Statement`
            The mapped Statement.
        """
        mapped_stmt = deepcopy(stmt)

        # Iterate over the agents
        # Update agents directly participating in the statement
        agent_list = mapped_stmt.agent_list()
        for idx, agent in enumerate(agent_list):
            # If the agent is None, we do nothing
            if agent is None:
                continue
            # If the agent's TEXT is in the ignores list, we return None to
            # then filter out the Statement
            agent_txt = agent.db_refs.get('TEXT')
            if agent_txt and agent_txt in self.ignores:
                return None

            # Check if an adeft model exists for agent text
            adeft_used = False
            if self.use_adeft and agent_txt and agent_txt in \
                    adeft_disambiguators:
                try:
                    run_adeft_disambiguation(mapped_stmt, agent, idx)
                    adeft_used = True
                except Exception as e:
                    logger.error('There was an error during Adeft'
                                 ' disambiguation of %s.' % agent_txt)
                    logger.error(e)

            # If adeft was not used, we do grounding mapping
            new_agent = self.map_agent(agent, do_rename) if not adeft_used \
                else agent

            # If the old agent had bound conditions, but the new agent does
            # not, copy the bound conditions over
            if new_agent is not None and len(new_agent.bound_conditions) == 0:
                new_agent.bound_conditions = agent.bound_conditions

            agent_list[idx] = new_agent

        mapped_stmt.set_agent_list(agent_list)

        # Update agents in the bound conditions
        for agent in agent_list:
            if agent is not None:
                for bc in agent.bound_conditions:
                    bc.agent = self.map_agent(bc.agent, do_rename)
                    if not bc.agent:
                        # Skip the entire statement if the agent maps to None
                        # in the grounding map
                        return None

        return mapped_stmt

    def map_agent(self, agent, do_rename):
        """Return the given Agent with its grounding mapped.

        This function grounds a single agent. It returns the new Agent object
        (which might be a different object if we load a new agent state
        from json) or the same object otherwise.

        Parameters
        ----------
        agent : :py:class:`indra.statements.Agent`
            The Agent to map.
        do_rename: bool
            If True, the Agent name is updated based on the mapped grounding.
            If do_rename is True the priority for setting the name is
            FamPlex ID, HGNC symbol, then the gene name
            from Uniprot.

        Returns
        -------
        grounded_agent : :py:class:`indra.statements.Agent`
            The grounded Agent.
        """
        # We always standardize DB refs as a functionality in the
        # GroundingMapper. If a new module is implemented which is
        # responsible for standardizing grounding, this can be removed.
        agent.db_refs = self.standardize_db_refs(agent.db_refs)
        # If there is no TEXT available, we can return immediately since we
        # can't do mapping
        agent_text = agent.db_refs.get('TEXT')
        if not agent_text:
            # We still do the name standardization here
            if do_rename:
                self.standardize_agent_name(agent, standardize_refs=False)
            return agent

        # 1. Check if there is a full agent mapping and apply if there is
        if agent_text in self.agent_map:
            mapped_to_agent = \
                Agent._from_json(self.agent_map[agent_text]['agent'])
            return mapped_to_agent

        # 2. Look agent text up in the grounding map
        if agent_text in self.grounding_map:
            self.update_agent_db_refs(agent, self.grounding_map[agent_text],
                                      do_rename)

        # 3. Look agent text up in the misgrounding map
        if agent_text in self.misgrounding_map:
            self.remove_agent_db_refs(agent, self.misgrounding_map[agent_text])
        # This happens when there is an Agent text but it is not in the
        # grounding map. We still do the name standardization here.
        if do_rename:
            self.standardize_agent_name(agent, standardize_refs=False)
        # Otherwise just return
        return agent

    def update_agent_db_refs(self, agent, db_refs, do_rename=True):
        """Update db_refs of agent using the grounding map

        If the grounding map is missing one of the HGNC symbol or Uniprot ID,
        attempts to reconstruct one from the other.

        Parameters
        ----------
        agent : :py:class:`indra.statements.Agent`
            The agent whose db_refs will be updated
        db_refs : dict
            The db_refs so set for the agent.
        do_rename: Optional[bool]
            If True, the Agent name is updated based on the mapped grounding.
            If do_rename is True the priority for setting the name is
            FamPlex ID, HGNC symbol, then the gene name
            from Uniprot. Default: True
        """
        # Standardize the IDs in the db_refs dict and set it as the Agent's
        # db_refs
        txt = agent.db_refs.get('TEXT')
        agent.db_refs = self.standardize_db_refs(deepcopy(db_refs))
        if txt:
            agent.db_refs['TEXT'] = txt
        # Finally, if renaming is needed we standardize the Agent's name
        if do_rename:
            self.standardize_agent_name(agent, standardize_refs=False)

    def remove_agent_db_refs(self, agent, db_refs):
        # Standardize the IDs in the db_refs dict and set it as the Agent's
        # db_refs
        standard_refs = self.standardize_db_refs(deepcopy(db_refs))
        # If there is any overlap between the Agent's db_refs and the db_refs
        # that are to be eliminated, we consider the Agent's db_refs to be
        # invalid and remove them. We then reset the Agent's name to
        # its TEXT value if available.
        agent_txt = agent.db_refs.get('TEXT')
        if set(standard_refs.items()) & set(agent.db_refs.items()):
            agent.db_refs = {}
            if agent_txt:
                agent.db_refs['TEXT'] = agent_txt
                agent.name = agent_txt

    @staticmethod
    def standardize_db_refs(db_refs):
        """Return a standardized db refs dict for a given db refs dict.

        Parameters
        ----------
        db_refs : dict
            A dict of db refs that may not be standardized, i.e., may be
            missing an available UP ID corresponding to an existing HGNC ID.

        Returns
        -------
        dict
            The db_refs dict with standardized entries.
        """
        up_id = db_refs.get('UP')
        hgnc_id = db_refs.get('HGNC')
        # If we have a UP ID and no HGNC ID, we try to get a gene name,
        # and if possible, a HGNC ID from that
        if up_id and not hgnc_id:
            hgnc_id = uniprot_client.get_hgnc_id(up_id)
            if hgnc_id:
                db_refs['HGNC'] = hgnc_id
        # Otherwise, if we don't have a UP ID but have an HGNC ID, we try to
        # get the UP ID
        elif hgnc_id:
            # Now get the Uniprot ID for the gene
            mapped_up_id = hgnc_client.get_uniprot_id(hgnc_id)
            if mapped_up_id:
                # If we find an inconsistency, we explain it in an error
                # message and fall back on the mapped ID
                if up_id and up_id != mapped_up_id:
                    # We handle a special case here in which mapped_up_id is
                    # actually a list of UP IDs that we skip and just keep
                    # the original up_id
                    if ', ' not in mapped_up_id:
                        # If we got a proper single protein mapping, we use
                        # the mapped_up_id to standardize to.
                        msg = ('Inconsistent groundings UP:%s not equal to '
                               'UP:%s mapped from HGNC:%s, standardizing to '
                               'UP:%s' % (up_id, mapped_up_id, hgnc_id,
                                          mapped_up_id))
                        logger.debug(msg)
                        db_refs['UP'] = mapped_up_id
                # If there is no conflict, we can update the UP entry
                else:
                    db_refs['UP'] = mapped_up_id

        # Now try to improve chemical groundings
        pc_id = db_refs.get('PUBCHEM')
        chebi_id = db_refs.get('CHEBI')
        hmdb_id = db_refs.get('HMDB')
        mapped_chebi_id = None
        mapped_pc_id = None
        hmdb_mapped_chebi_id = None
        # If we have original PUBCHEM and CHEBI IDs, we always keep those:
        if pc_id:
            mapped_chebi_id = chebi_client.get_chebi_id_from_pubchem(pc_id)
            if mapped_chebi_id and not mapped_chebi_id.startswith('CHEBI:'):
                mapped_chebi_id = 'CHEBI:%s' % mapped_chebi_id
        if chebi_id:
            mapped_pc_id = chebi_client.get_pubchem_id(chebi_id)
        if hmdb_id:
            hmdb_mapped_chebi_id = chebi_client.get_chebi_id_from_hmdb(hmdb_id)
            if hmdb_mapped_chebi_id and \
                    not hmdb_mapped_chebi_id.startswith('CHEBI:'):
                hmdb_mapped_chebi_id = 'CHEBI:%s' % hmdb_mapped_chebi_id
        # We always keep originals if both are present but display warnings
        # if there are inconsistencies
        if pc_id and chebi_id and mapped_pc_id and pc_id != mapped_pc_id:
            msg = ('Inconsistent groundings PUBCHEM:%s not equal to '
                   'PUBCHEM:%s mapped from %s, standardizing to '
                   'PUBCHEM:%s.' % (pc_id, mapped_pc_id, chebi_id, pc_id))
            logger.debug(msg)
        elif pc_id and chebi_id and mapped_chebi_id and chebi_id != \
                mapped_chebi_id:
            msg = ('Inconsistent groundings %s not equal to '
                   '%s mapped from PUBCHEM:%s, standardizing to '
                   '%s.' % (chebi_id, mapped_chebi_id, pc_id, chebi_id))
            logger.debug(msg)
        # If we have PC and not CHEBI but can map to CHEBI, we do that
        elif pc_id and not chebi_id and mapped_chebi_id:
            db_refs['CHEBI'] = mapped_chebi_id
        elif hmdb_id and chebi_id and hmdb_mapped_chebi_id and \
                hmdb_mapped_chebi_id != chebi_id:
            msg = ('Inconsistent groundings %s not equal to '
                   '%s mapped from %s, standardizing to '
                   '%s.' % (chebi_id, hmdb_mapped_chebi_id, hmdb_id, chebi_id))
            logger.debug(msg)
        elif hmdb_id and not chebi_id and hmdb_mapped_chebi_id:
            db_refs['CHEBI'] = hmdb_mapped_chebi_id
        # If we have CHEBI and not PC but can map to PC, we do that
        elif chebi_id and not pc_id and mapped_pc_id:
            db_refs['PUBCHEM'] = mapped_pc_id
        # Otherwise there is no useful mapping that we can add and no
        # further conflict to resolve.
        return db_refs

    @staticmethod
    def standardize_agent_name(agent, standardize_refs=True):
        """Standardize the name of an Agent based on grounding information.

        If an agent contains a FamPlex grounding, the FamPlex ID is used as a
        name. Otherwise if it contains a Uniprot ID, an attempt is made to find
        the associated HGNC gene name. If one can be found it is used as the
        agent name and the associated HGNC ID is added as an entry to the
        db_refs. Similarly, CHEBI, MESH and GO IDs are used in this order of
        priority to assign a standardized name to the Agent. If no relevant
        IDs are found, the name is not changed.

        Parameters
        ----------
        agent : indra.statements.Agent
            An INDRA Agent whose name attribute should be standardized based
            on grounding information.
        standardize_refs : Optional[bool]
            If True, this function assumes that the Agent's db_refs need to
            be standardized, e.g., HGNC mapped to UP.
            Default: True
        """
        # We return immediately for None Agents
        if agent is None:
            return

        if standardize_refs:
            agent.db_refs = GroundingMapper.standardize_db_refs(agent.db_refs)

        # We next look for prioritized grounding, if missing, we return
        db_ns, db_id = agent.get_grounding()
        if not db_ns or not db_id:
            return

        # If there's a FamPlex ID, prefer that for the name
        if db_ns == 'FPLX':
            agent.name = db_id
        # Importantly, HGNC here will be a symbol because that is what
        # get_grounding returns
        elif db_ns == 'HGNC':
            agent.name = hgnc_client.get_hgnc_name(db_id)
        elif db_ns == 'UP':
            # Try for the gene name
            gene_name = uniprot_client.get_gene_name(db_id, web_fallback=False)
            if gene_name:
                agent.name = gene_name
        elif db_ns == 'CHEBI':
            chebi_name = \
                chebi_client.get_chebi_name_from_id(db_id)
            if chebi_name:
                agent.name = chebi_name
        elif db_ns == 'MESH':
            mesh_name = mesh_client.get_mesh_name(db_id, False)
            if mesh_name:
                agent.name = mesh_name
        elif db_ns == 'GO':
            go_name = go_client.get_go_label(db_id)
            if go_name:
                agent.name = go_name
        return

    @staticmethod
    def rename_agents(stmts):
        """Return a list of mapped statements with updated agent names.

        Creates a new list of statements without modifying the original list.

        Parameters
        ----------
        stmts : list of :py:class:`indra.statements.Statement`
            List of statements whose Agents need their names updated.

        Returns
        -------
        mapped_stmts : list of :py:class:`indra.statements.Statement`
            A new list of Statements with updated Agent names
        """
        # Make a copy of the stmts
        mapped_stmts = deepcopy(stmts)
        # Iterate over the statements
        for _, stmt in enumerate(mapped_stmts):
            # Iterate over the agents
            for agent in stmt.agent_list():
                GroundingMapper.standardize_agent_name(agent, True)
        return mapped_stmts


# TODO: handle the cases when there is more than one entry for the same
# key (e.g., ROS, ER)
def load_grounding_map(grounding_map_path, lineterminator='\r\n',
                       hgnc_symbols=True):
    """Return a grounding map dictionary loaded from a csv file.

    In the file pointed to by grounding_map_path, the number of name_space ID
    pairs can vary per row and commas are
    used to pad out entries containing fewer than the maximum amount of
    name spaces appearing in the file. Lines should be terminated with \r\n
    both a carriage return and a new line by default.

    Optionally, one can specify another csv file (pointed to by ignore_path)
    containing agent texts that are degenerate and should be filtered out.

    It is important to note that this function assumes that the mapping file
    entries for the HGNC key are symbols not IDs. These symbols are converted
    to IDs upon loading here.

    Parameters
    ----------
    grounding_map_path : str
        Path to csv file containing grounding map information. Rows of the file
        should be of the form <agent_text>,<name_space_1>,<ID_1>,...
        <name_space_n>,<ID_n>
    lineterminator : Optional[str]
        Line terminator used in input csv file. Default: \r\n
    hgnc_symbols : Optional[bool]
        Set to True if the grounding map file contains HGNC symbols rather than
        IDs. In this case, the entries are replaced by IDs. Default: True

    Returns
    -------
    g_map : dict
        The grounding map constructed from the given files.
    """
    gmap = {}
    map_rows = read_unicode_csv(grounding_map_path, delimiter=',',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL,
                                lineterminator=lineterminator)
    for row in map_rows:
        txt = row[0]
        keys = [entry for entry in row[1::2] if entry]
        values = [entry for entry in row[2::2] if entry]
        if not keys or not values:
            logger.warning('Missing grounding entries for %s, skipping.' % txt)
            continue
        if len(keys) != len(values):
            logger.warning('Mismatched keys and values in row %s, skipping.' %
                           str(row))
            continue
        gmap[txt] = dict(zip(keys, values))
    if hgnc_symbols:
        gmap = replace_hgnc_symbols(gmap)
    return gmap


def replace_hgnc_symbols(gmap):
    """Replace HGNC symbols with IDs in a grounding map."""
    for txt, mapped_refs in deepcopy(gmap).items():
        hgnc_sym = mapped_refs.get('HGNC')
        if hgnc_sym:
            hgnc_id = hgnc_client.get_hgnc_id(hgnc_sym)
            # Override the HGNC symbol entry from the grounding
            # map with an HGNC ID
            if hgnc_id:
                mapped_refs['HGNC'] = hgnc_id
            else:
                logger.error('No HGNC ID corresponding to gene '
                             'symbol %s in grounding map.' % hgnc_sym)
                # Remove the HGNC symbol in this case
                mapped_refs.pop('HGNC')
        # In case the only grounding was eliminated, we remove the entry
        # completely
        if mapped_refs:
            gmap[txt] = mapped_refs
    return gmap


def _get_resource_path(*suffixes):
    return os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,
                        'resources', *suffixes)


def _load_default_grounding_map():
    default_grounding_map_path = \
        _get_resource_path('famplex', 'grounding_map.csv')
    gmap = load_grounding_map(default_grounding_map_path, hgnc_symbols=True)
    return gmap


def _load_default_misgrounding_map():
    default_misgrounding_map_path = \
        _get_resource_path('grounding', 'misgrounding_map.csv')
    gmap = load_grounding_map(default_misgrounding_map_path, hgnc_symbols=False)
    return gmap


def _load_default_agent_map():
    default_agent_grounding_path = \
        _get_resource_path('grounding', 'agents.json')
    with open(default_agent_grounding_path, 'r') as fh:
        agent_map = json.load(fh)
    return agent_map


def _load_default_ignores():
    default_ignore_path = _get_resource_path('grounding', 'ignore.csv')
    with open(default_ignore_path, 'r') as fh:
        ignores = [l.strip() for l in fh.readlines()]
    return ignores


default_grounding_map = _load_default_grounding_map()
gm = default_grounding_map  # For backwards compatibility, redundant
default_misgrounding_map = _load_default_misgrounding_map()
default_agent_map = _load_default_agent_map()
default_ignores = _load_default_ignores()
default_mapper = GroundingMapper(default_grounding_map,
                                 agent_map=default_agent_map,
                                 ignores=default_ignores,
                                 misgrounding_map=default_misgrounding_map)


from .adeft import adeft_disambiguators, run_adeft_disambiguation
