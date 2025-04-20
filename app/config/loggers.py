from app.utils.logger_utils import get_logger


app_logger =  get_logger("app","app.log")
llm_logger =  get_logger("llm","llm.log")
postgres_log =  get_logger("postgres","postgres.log")
milvus_logger =  get_logger("milvus","milvus.log")
