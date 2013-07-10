from boto.ec2 import EC2Connection, get_region
from fabric.colors import red

__author__ = 'mathos'


def ec2_digger():
    zones = ['us-east-1', 'us-west-2', 'us-west-1']

    server_dict = dict()
    tag_dict = dict()
    for zone in zones:
        ec2_conn = EC2Connection(region=get_region(zone))
        reservation = ec2_conn.get_all_instances()
        if len(reservation) <= 0:
            print red("No instances in " + zone + ", cool cat.")
        else:
            for r in reservation:
                for i in r.instances:
                    instance = dict()
                    status = i.update()
                    if status == "running":
                        instance['status'] = status
                        instance['zone'] = zone
                        if hasattr(i, 'tags'):
                            tags = getattr(i, 'tags')
                            for tag in tags:
                                if tag.lower() not in tag_dict:
                                    tag_dict[tag.lower()] = dict()
                                tag_vals = tag_dict[tag.lower()]
                                tag_val = tags.get(tag)
                                if tag_val.lower() not in tag_vals:
                                    tag_vals[tag_val.lower()] = []
                                tag_vals[tag_val.lower()].append(getattr(i, 'dns_name'))

                        methods = dir(i)
                        for method in methods:
                            if not method.startswith("_"):
                                if not hasattr(getattr(i, method), "__call__"):
                                    if method == 'block_device_mapping':
                                        blocks = getattr(i, method)
                                        block_dict = dict()
                                        for device in blocks:
                                            block_dict[device] = blocks.get(device).volume_id
                                        instance[method] = block_dict
                                    elif method == 'groups':
                                        groups = getattr(i, method)
                                        new_groups = list()
                                        for group in groups:
                                            new_groups.append(group.name)
                                        instance[method] = new_groups
                                    else:
                                        instance[method] = getattr(i, method)
                        server_dict[instance.get('dns_name')] = instance

    return server_dict, tag_dict
