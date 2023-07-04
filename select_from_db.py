def get_user(username, password):
    sql = f"select username from user where username={usernmae} and password={password}"
    res = query(sql)
    return res