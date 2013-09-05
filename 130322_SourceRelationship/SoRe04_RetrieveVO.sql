--TB_M00_MVC_SERVICES
--TB_M00_MVC_PROCESS           : list all processes
--TB_M00_MVC_ACTIVITY_LINES    : process details information
--TB_M00_MVC_ACTIVITY_DETAILS  : binding variables
--tb_m00_activity_components
--TB_M00_MVC_ACTIVITY_HEADERS
--@@@@@@
--$$$$$$
select new_process_lov.MVC_SERVICE_NM,
       new_process_lov.MVC_PROCESS_ID,
       new_process_lov.ACTIVITY_COMPONENT_NM,
       new_process_lov.ACTIVITY_HEADER_ID,
       new_process_lov.MVC_PROCESS_NM,
       activity.VO_NM,
       activity.DML_WHERE_CLAUSE DML_WHERE_CLAUSE,
       activity.RESULT_NM RESULT_NM$$$$$$,
       activity.*
from   TB_M00_MVC_ACTIVITY_LINES activity,
       (select MVC_SERVICE_NM,
               ACTIVITY_HEADER_ID,
               MVC_PROCESS_ID,
               MVC_PROCESS_NM,
               ACTIVITY_COMPONENT_NM
        from   tb_m00_mvc_process,
               TB_M00_ACTIVITY_COMPONENTS,
               TB_M00_MVC_SERVICES
        where  1=1
            and tb_m00_mvc_process.mvc_service_id = TB_M00_MVC_SERVICES.mvc_service_id
            and tb_m00_mvc_process.COMPONENT_ID = TB_M00_ACTIVITY_COMPONENTS.COMPONENT_ID
            and MVC_SERVICE_NM like 'm800505069pop1%'
            and TB_M00_MVC_SERVICES.END_ACTIVE_DATE = TO_DATE('29991231235959', 'YYYYMMDDHH24MISS') 
        ) new_process_lov
where  activity.ACTIVITY_HEADER_ID = new_process_lov.ACTIVITY_HEADER_ID
--and ACTIVITY_COMPONENT_NM like 'SendMessage%'
order by new_process_lov.MVC_SERVICE_NM, new_process_lov.MVC_PROCESS_NM
;
