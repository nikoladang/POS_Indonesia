In order to apply for this job:
- All JAVA files inside src_path = root + '\src' have to be in UTF-8 encoding
- Import file in JSP must stand in one line
   BAD
       <%@ page import="com.posco.mes.m80.common.helper.PosAggregationHelper,
                 com.posco.mes.m80.common.bl.bc4j.vo.common.PosYardViewObject,
                 com.posco.mes.m84.p050.app.constants.PosM800505000ConstantsIF"%>
   good
       <%@ page import="com.posco.mes.m80.common.helper.PosAggregationHelper" %>
       <%@ page import="com.posco.mes.m80.common.bl.bc4j.vo.common.PosYardViewObject" %>
       <%@ page import="com.posco.mes.m84.p050.app.constants.PosM800505000ConstantsIF" %>


--Job03_RetrieveJavaSourceRelateToScreen_00_output-----------
pgm_tp | pgm_id | javapackagefilename

==Troubleshoot===============================================
- Error
    conn = cx_Oracle.connect(connstr)
    cx_Oracle.DatabaseError: ORA-24315: 속성 유형이 부적당합니다
- Solution: install cx_Oracle 10g,  although connect to 11g DB