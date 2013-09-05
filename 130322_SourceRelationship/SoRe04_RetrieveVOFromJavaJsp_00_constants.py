"""
add(String viewObjectName, Map map)
add(String viewObjectName, Map map, String dmlTransactionMode)
addBeforeGet(String viewObjectName, Map map)
addBeforeGet(String viewObjectName, Map map, String dmlTransactionMode)
modify(String viewObjectName, String whereClause, Object whereClauseParams[], Map map)
modify(String viewObjectName, String whereClause, Object whereClauseParams[], Map map, boolean isClearFlag)
modify(String viewObjectName, String whereClause, Object whereClauseParams[], Map map, String dmlTransactionMode)
modify(String viewObjectName, String whereClause, Object whereClauseParams[], Map map, String dmlTransactionMode, boolean isClearFlag)
countModify(String viewObjectName, String whereClause, Object whereClauseParams[], Map map)
countModify(String viewObjectName, String whereClause, Object whereClauseParams[], Map map, boolean isClearFlag)
countModify(String viewObjectName, String whereClause, Object whereClauseParams[], Map map, String dmlTransactionMode)
countModify(String viewObjectName, String whereClause, Object whereClauseParams[], Map map, String dmlTransactionMode, boolean isClearFlag)
remove(String viewObjectName, Object id)
removeByTransaction(String viewObjectName, Object id, String dmlTransactionMode)
remove(String viewObjectName, String whereClause, Object whereClauseParams[])
remove(String viewObjectName, String whereClause, Object whereClauseParams[], boolean isClearFlag)
remove(String viewObjectName, String whereClause, Object whereClauseParams[], String dmlTransactionMode)
remove(String viewObjectName, String whereClause, Object whereClauseParams[], String dmlTransactionMode, boolean isClearFlag)
countRemove(String viewObjectName, String whereClause, Object whereClauseParams[])
countRemove(String viewObjectName, String whereClause, Object whereClauseParams[], boolean isClearFlag)
countRemove(String viewObjectName, String whereClause, Object whereClauseParms[], String dmlTransactionMode)
countRemove(String viewObjectName, String whereClause, Object whereClauseParms[], String dmlTransactionMode, boolean isClearFlag)
findBusinessObject(String viewObjectName, Object id)
findAllBusinessObjects(String viewObjectName)
findAllBusinessObjects(String viewObjectName, boolean isClearFlag)
findRestrictedBusinessObjects(String viewObjectName, String whereClause, Object whereClauseParams[], boolean isForwardOnly)
findRestrictedBusinessObjects(String viewObjectName, String whereClause, Object whereClauseParams[], boolean isForwardOnly, boolean isClearFlag)
findRestrictedBusinessObjects(String viewObjectName, String whereClause, Object whereClauseParams[], String orderBy, boolean isForwardOnly)
findRestrictedBusinessObjects(String viewObjectName, String whereClause, Object whereClauseParams[], String orderBy, boolean isForwardOnly, boolean isClearFlag)
findDetailBusinessObjects(String viewObjectName, String whereClause, Object whereClauseParams[], boolean isForwardOnly)
findDetailBusinessObjects(String viewObjectName, String whereClause, Object whereClauseParams[], boolean isForwardOnly, boolean isClearFlag)
findMasterBusinessObjects(String viewObjectName, String whereClause, Object whereClauseParams[], boolean isForwardOnly)
findMasterBusinessObjects(String viewObjectName, String whereClause, Object whereClauseParams[], boolean isForwardOnly, boolean isClearFlag)
upsert(ArrayList arrayList, String viewObjectName)
upsert(ArrayList arrayList, String viewObjectName, int upsertLockWaitTime)
upsert(ArrayList arrayList, String viewObjectName, boolean doPostChange)
upsert(ArrayList arrayList, String viewObjectName, int upsertLockWaitTime, boolean doPostChange)
executeSingleQuery(String stmt, List bindValues, DBTransaction trans) throws SQLException
executeQuery(String stmt, List bindValues, DBTransaction trans) throws SQLException
doQueryRows(String stmt, List bindValues, DBTransaction trans) throws SQLException
convertQuery(String stmt, List bindValues)
"""
functionsContainVOz = [
r'add *\(',
r'addBeforeGet *\(',
r'modify *\(',
r'countModify *\(',
r'remove *\(',
r'removeByTransaction *\(',
r'countRemove *\(',
r'findBusinessObject *\(',
r'findAllBusinessObjects *\(',
r'findRestrictedBusinessObjects *\(',
r'findDetailBusinessObjects *\(',
r'findMasterBusinessObjects *\(',

r'upsert *\(',

r'executeSingleQuery *\(',
r'executeQuery *\(',
r'doQueryRows *\(',
r'convertQuery *\(',
]

functionsContainVO = [
r'\.add *\(.*,',    #
r'\.addBeforeGet *\(',
r'\.modify *\(.*,',     #
r'\.countModify *\(',
r'\.remove *\(.*,',     #
r'\.removeByTransaction *\(',
r'\.countRemove *\(',
r'\.findBusinessObject *\(',
r'\.findAllBusinessObjects *\(',
r'\.findRestrictedBusinessObjects *\(',
r'\.findDetailBusinessObjects *\(',
r'\.findMasterBusinessObjects *\(',

r'\.upsert *\(',

r'\.executeSingleQuery *\(',
r'\.executeQuery *\(',
r'\.doQueryRows *\(',
r'\.convertQuery *\(',
]