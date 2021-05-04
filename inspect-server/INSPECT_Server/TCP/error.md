# ERROR_MESSAGE
## p_fm_work_check_barcode_and
1. 请传入正确的JSON字符串
2. 没有测试明细
3. 输入的条码为空。
4. 没有指定生产任务。
5. 没有指定工序。
6. 指定生产任务不存在。
7. 指定工序不存在。
8. 此序列号已经锁定不允许过站。
9. 工艺流程没有设定起始工序。
10. 工序<' + @sequence + '>不属于工艺流程<' + @process_code + '-' + @process_name + '>。
11. 工序<' + @sequence + '>未设定作业类型。
12. 工序<' + @sequence + '>未设定加工批量。
13. 条码<' + @barcode + '>还没有完成<' + @prev_proc_name + '>工艺流程的作业。
14. W:该条码距离<' + @seq_name+ '>作业已超过'+ CAST(@max_interval AS VARCHAR)+ '分钟。
16. 2.条码<' + @barcode + '>没有作业记录，请从<'+ ISNULL(@first_seq_name, '') + '>工序开始执行。
17. A11条码<' + @barcode + '>当前执行工序为<'+ ISNULL(@seq_name, '') + '>。
18. 条码<' + @barcode+ '>当前执行工序已经过站，下一站为<' + ISNULL(@seq_name,'') + '>。
19. A0条码<' + @barcode + '>当前执行工序为<'+ ISNULL(@seq_name, '') + '>。'+CAST(@sequence_id AS NVARCHAR(10))+'你选择工序为：'+@local_seq_name
20. 该条码已经结束作业。
21. 与前工序<' + @from_seq_name + '>执行间隔不足'+ CAST(@min_interval AS VARCHAR) + '分钟，请'+ CAST(DATEDIFF(MINUTE, GETDATE(),DATEADD(mi, @min_interval,@from_work_time)) AS VARCHAR)+ '分钟后再执行。
24. 该条码['+@barcode+']的前缀不符合该生产任务的前缀定义规则。
25. 该条码的后缀不符合该工单的后缀定义规则。
26. 该条码字符长度为“'+CAST(LEN(@barcode) AS NVARCHAR(10))+'”，而该生产任务的编码规则定义字符长度为“'+CAST(@TM_WS AS NVARCHAR(10))
27. 该条码流水码范围为“'+CAST(@sn_begin AS NVARCHAR(10))+'”到“'+CAST(@sn_end AS NVARCHAR(10))+'”，而该条码流水号为“'+CAST(@s_no_str AS NVARCHAR(10))+'”，不符合编码规则定义。
28. 条码“'+@barcode+'”不属于当前工单。
29. 该生产任务没有定义条码规则，且扫描条码又不属于镭雕二维码编码！

## p_fm_work_create_for_test
1. insert_into_fm_work_inspect_table_fail
2. MES测试程序工序代码['+@sequence_code+']，测试程序输出的工序代码：['+@Test_Process+']
3. MES测试中，项目“'+ISNULL(@inspect_title, '')+'”的值为“'+ISNULL(@inspect_value, '')+'”，而该生产任务产品的相应的值为“'+ISNULL(@chip_version, '')+'”。 
4. MES测试程序产品编码['+@item_code+']，测试程序输出的产品编码：['+@item_number+']
5. 生产任务没有指定QC工程图。11111'+@task_order_code
6. 工序<'+@sequence_code+'>不存在。
7. 没有指定PASS流向工序。
8. 没有指定FAIL流向工序。
9. '<'+@result+'>为非预期的测试结果。