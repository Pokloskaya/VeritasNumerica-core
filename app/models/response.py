def ResponseModel(data, success, error):
    if not success:
        return {
            "success": success,
            "error": error,
        }
    return {
        "success": success,
        "data": data,
    }
