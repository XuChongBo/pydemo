def action1():
    return "this is the first cgi.  action1"


def action2():
    return "this the second cgi. action 2"


def action3():
    return HTML(BODY(H2("abc"),
        H2(A('入库',_href=URL('upload'))),
        H2(A('检索',_href=URL('retrieval')))
        ))
