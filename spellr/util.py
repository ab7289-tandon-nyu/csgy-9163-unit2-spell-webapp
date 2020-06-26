def get_flash_msg(error=None, success=None):
    if error is not None:
        return (error, "error")
    elif success is not None:
        return (success, "success")
    return None
