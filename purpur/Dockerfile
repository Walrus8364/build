# purpur/Dockerfile

# 使用官方的 GraalVM CE 镜像，它本身就是多架构的
FROM ghcr.io/graalvm/jdk:java17

# 定义构建参数，可以从 build-push-action 传入
ARG MC_VERSION=1.20.4
ARG PURPUR_JAR_NAME=purpur.jar

# 设置工作目录
WORKDIR /workspace

# 安装 curl 用于下载，并清理缓存
RUN microdnf install curl && \
    microdnf clean all

# 下载 Purpur 服务端
RUN curl -L -o ${PURPUR_JAR_NAME} \
    "https://api.purpurmc.org/v2/purpur/${MC_VERSION}/latest/download"

# 复制启动脚本到镜像中
COPY start.sh .

# 给予启动脚本执行权限
RUN chmod +x start.sh

# 声明服务器数据卷，用于持久化世界、插件等数据
VOLUME /workspace

# 暴露 Minecraft 服务器端口
EXPOSE 25565

# 设置容器启动时执行的命令
CMD ["./start.sh"]