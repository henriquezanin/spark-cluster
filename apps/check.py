# %%
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .master('spark://spark-master:7077')
    .appName("spark_test")
    .getOrCreate()
)
# particoes de memoria
spark.conf.set("spark.sql.shuffle.partitions", 6)

# %%
# simple query
spark.sql("select now();")

# %%
# load data


def spark_read_csv(filename):
    return spark.read.options(
        sep="|", inferSchema=True, header=True).csv(filename)


# esta no arquivo local
exames = spark.read.load('/data/bpsp_exames.parquet')
exames.createOrReplaceTempView("exames")

# %%
# mostrar tabela carregada
spark.sql("select * from exames limit 10").show()

# %%
# a shuffle operation
spark.sql("""
    select max(id_paciente) , count(*)
    from exames
    group by id_paciente
    order by 2 desc;
""").limit(10).show()
