# purpur/Dockerfile

ARG BASE_IMAGE=container-registry.oracle.com/graalvm/jdk:17
# 使用变量作为基础镜像
FROM ${BASE_IMAGE}

# 定义构建参数，可以从 build-push-action 传入
ARG MC_VERSION=1.20.4
ARG PURPUR_JAR_NAME=purpur.jar


# 安装 curl 用于下载，并清理缓存
RUN mkdir /app && \
    microdnf install curl && \
    microdnf clean all

# 下载 Purpur 服务端
RUN curl -L -o /app/${PURPUR_JAR_NAME} \
    "https://api.purpurmc.org/v2/purpur/${MC_VERSION}/latest/download"

# 复制启动脚本到镜像中
COPY start.sh /app/start.sh

# 给予启动脚本执行权限
RUN chmod +x /app/start.sh

# 声明服务器数据卷，用于持久化世界、插件等数据
VOLUME /workspace

# 暴露 Minecraft 服务器端口
EXPOSE 25565

# 设置容器启动时执行的命令
CMD ["/app/start.sh"]