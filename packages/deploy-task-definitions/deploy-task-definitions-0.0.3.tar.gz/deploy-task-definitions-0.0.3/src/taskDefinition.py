def get_environment_variables(config):
    env_keys = list(filter(lambda variable: variable.startswith('ENV_'), config.keys()))
    return list(map(lambda key: {'name': key.replace('ENV_',''), 'value': config[key]}, env_keys))

def get_task_definition(config):

    task =  {
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                'awslogs-group': config['FAMILY'],
                'awslogs-region': config['REGION']
            }
        },
        "portMappings": [],
        "cpu": int(config['TASK_CPU']),
        "memory": int(config['TASK_MEMORY']),
        "image": config['TASK_IMAGE'],
        "essential": True,
        "name": config['TASK_NAME'],
        "environment": get_environment_variables(config),
        "entryPoint": eval(config['ENTRYPOINT']),
        "command": eval(config['COMMAND']),
        "links": []
    }

    if "TASK_MEMORY_RESERVATION" in config:
        task["memoryReservation"] = int(config['TASK_MEMORY_RESERVATION'])

    if "PORT_MAPPING_CONTAINER_PORT" in config:
        task["portMappings"].append({
            "containerPort": int(config['PORT_MAPPING_CONTAINER_PORT']),
            "hostPort": int(config['PORT_MAPPING_HOST_PORT']),
            "protocol": config['PORT_MAPPING_PROTOCOL'],
        })
    return [task]

