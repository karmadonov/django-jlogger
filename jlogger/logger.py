from models import JLogger

def debug(msg):
    return JLogger().log('D', msg)

def info(msg):
    return JLogger().log('I', msg)

def warning(msg):
    return JLogger().log('W', msg)

def error(msg):
    return JLogger().log('E', msg)

def critical(msg):
    return JLogger().log('C', msg)

def log(level, msg):
    return JLogger().log(level, msg)