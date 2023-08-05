import boto3
import logging
import requests
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from indra import get_config, has_config
from indra.util.nested_dict import NestedDict

logger = logging.getLogger(__name__)


def get_ids(job_list):
    if job_list is None:
        return None
    return [job['jobId'] for job in job_list]


def kill_all(job_queue, reason='None given', states=None, kill_list=None):
    """Terminates/cancels all jobs on the specified queue.

    Parameters
    ----------
    job_queue : str
        The name of the Batch job queue on which you wish to terminate/cancel
        jobs.
    reason : str
        Provide a reason for the kill that will be recorded with the job's
        record on AWS.
    states : None or list[str]
        A list of job states to remove. Possible states are 'STARTING',
        'RUNNABLE', and 'RUNNING'. If None, all jobs in all states will be
        ended (modulo the `kill_list` below).
    kill_list : None or list[dict]
        A list of job dictionaries (as returned by the submit function) that
        you specifically wish to kill. All other jobs on the queue will be
        ignored. If None, all jobs on the queue will be ended (modulo the
        above).

    Returns
    -------
    killed_ids : list[str]
        A list of the job ids for jobs that were killed.
    """
    # Default is all states.
    if states is None:
        states = ['STARTING', 'RUNNABLE', 'RUNNING']

    # Get batch client
    batch = boto3.client('batch')

    # Get all other jobs, and terminate them.
    killed_ids = []
    for status in states:
        running = batch.list_jobs(jobQueue=job_queue, jobStatus=status)
        active_job_list = running.get('jobSummaryList')
        if active_job_list is None:
            continue

        for job in active_job_list:
            # Check if this is one of the specified jobs, if any specified.
            ids_to_kill = get_ids(kill_list)
            if ids_to_kill is not None and job['jobId'] not in ids_to_kill:
                continue

            # End the job.
            if status == 'RUNNING':
                logger.info('Terminating {jobName} ({jobId})'.format(**job))
                res = batch.terminate_job(jobId=job['jobId'], reason=reason)
            else:
                logger.info('Canceling {jobName} ({jobId})'.format(**job))
                res = batch.cancel_job(jobId=job['jobId'], reason=reason)

            # Record the result of the kill
            killed_ids.append(res)

    return killed_ids


def tag_instance(instance_id, **tags):
    """Tag a single ec2 instance."""
    logger.debug("Got request to add tags %s to instance %s."
                 % (str(tags), instance_id))
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instance_id)

    # Remove None's from `tags`
    filtered_tags = {k: v for k, v in tags.items() if v and k}

    # Check for existing tags
    if instance.tags is not None:
        existing_tags = {tag.get('Key'): tag.get('Value')
                         for tag in instance.tags}
        logger.debug("Ignoring existing tags; %s" % str(existing_tags))
        for tag_key in existing_tags.keys():
            filtered_tags.pop(tag_key, None)

    # If we have new tags to add, add them.
    tag_list = [{'Key': k, 'Value': v} for k, v in filtered_tags.items()]
    if len(tag_list):
        logger.info('Adding project tags "%s" to instance %s'
                    % (filtered_tags, instance_id))
        instance.create_tags(Tags=tag_list)
        vols = instance.volumes.all()
        for page in vols.pages():
            for vol in page:
                vol.create_tags(Tags=tag_list)
    else:
        logger.info('No new tags from: %s' % str(tags))
    return


def tag_myself(project='cwc', **other_tags):
    """Function run when indra is used in an EC2 instance to apply tags."""
    base_url = "http://169.254.169.254"
    try:
        resp = requests.get(base_url + "/latest/meta-data/instance-id")
    except requests.exceptions.ConnectionError:
        logger.warning("Could not connect to service. Note this should only "
                       "be run from within a batch job.")
        return
    instance_id = resp.text
    tag_instance(instance_id, project=project, **other_tags)
    return


def get_batch_command(command_list, project=None, purpose=None):
    """Get the command appropriate for running something on batch."""
    command_str = ' '.join(command_list)
    ret = ['python', '-m', 'indra.util.aws', 'run_in_batch', command_str]
    if not project and has_config('DEFAULT_AWS_PROJECT'):
        project = get_config('DEFAULT_AWS_PROJECT')
    if project:
        ret += ['--project', project]
    if purpose:
        ret += ['--purpose', purpose]
    return ret


def run_in_batch(command_list, project, purpose):
    from subprocess import call
    tag_myself(project, purpose=purpose)
    logger.info('\n'+20*'='+' Begin Primary Command Output '+20*'='+'\n')
    ret_code = call(command_list)
    logger.info('\n'+21*'='+' End Primary Command Output '+21*'='+'\n')
    return ret_code


def get_jobs(job_queue='run_reach_queue', job_status='RUNNING'):
    """Returns a list of dicts with jobName and jobId for each job with the
    given status."""
    batch = boto3.client('batch')
    jobs = batch.list_jobs(jobQueue=job_queue, jobStatus=job_status)
    return jobs.get('jobSummaryList')


def get_job_log(job_info, log_group_name='/aws/batch/job',
                write_file=True, verbose=False):
    """Gets the Cloudwatch log associated with the given job.

    Parameters
    ----------
    job_info : dict
        dict containing entries for 'jobName' and 'jobId', e.g., as returned
        by get_jobs()
    log_group_name : string
        Name of the log group; defaults to '/aws/batch/job'
    write_file : boolean
        If True, writes the downloaded log to a text file with the filename
        '%s_%s.log' % (job_name, job_id)


    Returns
    -------
    list of strings
        The event messages in the log, with the earliest events listed first.
    """
    job_name = job_info['jobName']
    job_id = job_info['jobId']
    logs = boto3.client('logs')
    batch = boto3.client('batch')
    resp = batch.describe_jobs(jobs=[job_id])
    job_desc = resp['jobs'][0]
    job_def_name = job_desc['jobDefinition'].split('/')[-1].split(':')[0]
    task_arn_id = job_desc['container']['taskArn'].split('/')[-1]
    log_stream_name = '%s/default/%s' % (job_def_name, task_arn_id)
    stream_resp = logs.describe_log_streams(
                            logGroupName=log_group_name,
                            logStreamNamePrefix=log_stream_name)
    streams = stream_resp.get('logStreams')
    if not streams:
        logger.warning('No streams for job')
        return None
    elif len(streams) > 1:
        logger.warning('More than 1 stream for job, returning first')
    log_stream_name = streams[0]['logStreamName']
    if verbose:
        logger.info("Getting log for %s/%s" % (job_name, job_id))
    out_file = ('%s_%s.log' % (job_name, job_id)) if write_file else None
    lines = get_log_by_name(log_group_name, log_stream_name, out_file, verbose)
    return lines


def get_log_by_name(log_group_name, log_stream_name, out_file=None,
                    verbose=True):
    """Download a log given the log's group and stream name.

    Parameters
    ----------
    log_group_name : str
        The name of the log group, e.g. /aws/batch/job.

    log_stream_name : str
        The name of the log stream, e.g. run_reach_jobdef/default/<UUID>

    Returns
    -------
    lines : list[str]
        The lines of the log as a list.
    """
    logs = boto3.client('logs')
    kwargs = {'logGroupName': log_group_name,
              'logStreamName': log_stream_name,
              'startFromHead': True}
    lines = []
    while True:
        response = logs.get_log_events(**kwargs)
        # If we've gotten all the events already, the nextForwardToken for
        # this call will be the same as the last one
        if response.get('nextForwardToken') == kwargs.get('nextToken'):
            break
        else:
            events = response.get('events')
            if events:
                lines += ['%s: %s\n' % (evt['timestamp'], evt['message'])
                          for evt in events]
            kwargs['nextToken'] = response.get('nextForwardToken')
        if verbose:
            logger.info('%d %s' % (len(lines), lines[-1]))
    if out_file:
        with open(out_file, 'wt') as f:
            for line in lines:
                f.write(line)
    return lines


def dump_logs(job_queue='run_reach_queue', job_status='RUNNING'):
    """Write logs for all jobs with given the status to files."""
    jobs = get_jobs(job_queue, job_status)
    for job in jobs:
        get_job_log(job, write_file=True)


def iter_s3_keys(s3, bucket, prefix):
    """Iterate over the keys in an s3 bucket given a prefix."""
    is_truncated = True
    marker = None
    while is_truncated:
        if marker:
            resp = s3.list_objects(Bucket=bucket, Prefix=prefix, Marker=marker)
        else:
            resp = s3.list_objects(Bucket=bucket, Prefix=prefix)
        for entry in resp['Contents']:
            if entry['Key'] != marker:
                yield entry['Key']

        is_truncated = resp['IsTruncated']
        marker = entry['Key']


def get_s3_file_tree(s3, bucket, prefix):
    """Overcome s3 response limit and return NestedDict tree of paths.

    The NestedDict object also allows the user to search by the ends of a path.

    The tree mimics a file directory structure, with the leave nodes being the
    full unbroken key. For example, 'path/to/file.txt' would be retrieved by

        ret['path']['to']['file.txt']['key']

    The NestedDict object returned also has the capability to get paths that
    lead to a certain value. So if you wanted all paths that lead to something
    called 'file.txt', you could use

        ret.get_paths('file.txt')

    For more details, see the NestedDict docs.
    """
    file_tree = NestedDict()
    pref_path = prefix.split('/')[:-1]   # avoid the trailing empty str.
    for key in iter_s3_keys(s3, bucket, prefix):
        full_path = key.split('/')
        relevant_path = full_path[len(pref_path):]
        curr = file_tree
        for step in relevant_path:
            curr = curr[step]
        curr['key'] = key
    return file_tree


if __name__ == '__main__':
    parser = ArgumentParser(
        'aws.py',
        description=('Use some of INDRA\'s aws tools. For more specific help, '
                     'select one of the Methods with the `-h` option.')
        )
    subparsers = parser.add_subparsers(title='Task')
    subparsers.required = True
    subparsers.dest = 'task'

    # Create parent parser classes for second layer of options
    parent_run_parser = ArgumentParser(add_help=False)
    parent_run_parser.add_argument(
        'command',
        help=('Enter the command as a single string to be run as if in a '
              'batch environment.')
        )
    parent_run_parser.add_argument(
        '--project', '-P',
        default='cwc',
        help='Give a name for the project.'
        )
    parent_run_parser.add_argument(
        '--purpose', '-p',
        help='Give the task some meaning.'
        )
    parent_kill_parser = ArgumentParser(add_help=False)
    parent_kill_parser.add_argument(
        'queue_name',
        help='Select the batch queue in which all jobs should be terminated.'
        )
    parent_kill_parser.add_argument(
        '--reason', '-R',
        help='Give a reason for killing all the jobs.'
        )
    # Make non_db_parser and get subparsers
    run_parser = subparsers.add_parser(
        'run_in_batch',
        parents=[parent_run_parser],
        description=('This should be called to run any command wtihin an aws '
                     'batch job instance.'),
        formatter_class=ArgumentDefaultsHelpFormatter
        )

    # Make db parser and get subparsers.
    kill_parser = subparsers.add_parser(
        'kill_all',
        parents=[parent_kill_parser],
        description='Kill all the jobs running in a given queue.',
        formatter_class=ArgumentDefaultsHelpFormatter
        )
    args = parser.parse_args()

    if args.task == 'run_in_batch':
        ret_code = run_in_batch(args.command.split(' '), args.project,
                                args.purpose)
        if ret_code is 0:
            logger.info('Job endend well.')
        else:
            logger.error('Job failed!')
            import sys
            sys.exit(ret_code)
    elif args.task == 'kill_all':
        kill_all(args.queue_name, args.reason)
