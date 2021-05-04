import json
from json import JSONDecodeError
from Inspect_Server.settings import RETEST
from Inspect_Server.log_setting import logger
from database.database_connect import DatabasePool, Parameters


def getparsedate(msg):
    msg_str = msg.decode('GBK').replace(b'\x00'.decode(),'')
    logger.info(msg_str)
    try:
        msg_dic = json.loads(msg_str)
    except JSONDecodeError as e:
        logger.error(e)
        return e
    return msg_dic


def checkbarcode(msg_dic):
    taskorder = msg_dic.get('taskorder', '')
    sequence = msg_dic.get('sequence', '')
    barcode = msg_dic.get('barcode', '')

    # TODO: p_fm_work_check_barcode_and
    sql = '''
                EXEC p_fm_work_check_barcode_and @taskorder,@sequence,'',@barcode,'MAIN'
                '''

    p = Parameters().add('taskorder', taskorder).add('sequence', sequence).add('barcode', barcode)

    connect = DatabasePool('X1_CORE_PROD')
    lists = connect.ExecuteQuery(sql, p)

    rtnstr = lists[0].get('rtnstr', '')
    if rtnstr != 'OK':
        logger.error(rtnstr)
    return rtnstr


def savetestdata(msg_dic, retest=RETEST):
    barcode = msg_dic.get('barcode', '')
    result = msg_dic.get('result', '')
    taskorder = msg_dic.get('taskorder', '')
    workline = msg_dic.get('workline', '')
    workstation = msg_dic.get('workstation', '')
    workshift = msg_dic.get('workshift', '')
    sequence = msg_dic.get('sequence', '')
    workdevice = msg_dic.get('workdevice', '')
    worker = msg_dic.get('worker', '')
    workleader = msg_dic.get('workleader', '')
    department = msg_dic.get('department', '')
    usercode = msg_dic.get('usercode', '')
    details = msg_dic.get('details', '')

    if details:
        details = details.replace("'", '"')

    # TODO: p_fm_work_create_for_test
    sql = '''
                EXEC p_fm_work_create_for_test @taskorder,@workline,@workstation,@workshift,@workdevice,@department,
                @sequence,@worker,@workleader,@barcode,@result,'',@details,NULL,@retest,@usercode,0
                '''

    p = Parameters().add('taskorder', taskorder).add('workline', workline).add('workstation', workstation)
    p.add('workshift', workshift).add('workdevice', workdevice).add('department', department)
    p.add('sequence', sequence).add('worker', worker).add('workleader', workleader).add('barcode', barcode)
    p.add('result', result).add('details', details).add('usercode', usercode).add('retest', retest)

    connect = DatabasePool('X1_CORE_DATA')
    res = connect.ExecuteQuery(sql, p)

    if isinstance(res, Exception):
        try:
            rtnstr = res.args[1].decode('UTF-8')
            logger.error(rtnstr)
        except IndexError as e:
            rtnstr = '允许重新测试一次'
            retest -= 1
    else:
        rtnstr = 'OK'

    return rtnstr
