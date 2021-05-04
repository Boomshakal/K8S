{"barcode": "YQX320000000011", "result": "PASS", "taskorder": "MO18020037-02", "workline": "Line2","workstation": "AS", "workshift": "白班", "sequence": "M082", "workdevice": "", "worker": "m00000873","workleader": "M00000760", "department": "部件", "usercode": "m00000873","details": "<items><item step='1' item='耐压测试' title='安规测试' max='1111' min='123321' value='123' result='PASS' unit='mA' time='2019-12-17' /><item step='2' item='绝缘测试' title='安规测试' max='1111' min='123321' value='123' result='PASS' unit='mA' time='2019-12-17' /><item step='3' item='泄漏测试' title='安规测试' max='1111' min='123321' value='123' result='PASS' unit='mA' time='2019-12-17' /></items>"}



### x1_core_prod.dbo.p_fm_work_check_barcode_and
```
exec x1_core_prod.dbo.p_fm_work_check_barcode_and
'MO18020037-02',
'M082',
'',
'YQX320000000011',
'MAIN'
```
### x1_core_data.dbo.p_fm_work_create_for_test
```
exec x1_core_data.dbo.p_fm_work_create_for_test 
'MO18020037-02',
'Line2（包装）',
'AS',
'白班',
'', --设备名称
'IKAHE', --部门
'M082', --工序
'm00000873',  --作业员工号
'M00000760',  --线长
'YQX320000000011', --入测条码
'PASS',  --结果
'', --用不到了
'<items>
<item step="0" item="安规测试" title="安规测试" max="1111" min="123321" value="123" result="PASS" unit="mA" time="2019-12-17"/>
</items>',  --测试明细
null,  --txt文件
0, --是否重试
'm00000873', --工号
'' --是否调试
```