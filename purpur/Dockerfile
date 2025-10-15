# purpur/Dockerfile

ARG BASE_IMAGE=ghcr.io/graalvm/jdk:java17
FROM ${BASE_IMAGE}

ARG MC_VERSION=1.20.4
ARG PURPUR_JAR_NAME=purpur.jar

# 1. 创建一个独立的 /app 目录来存放不会被覆盖的程序文件
RUN mkdir /app && microdnf install -y curl && microdnf clean all

# 2. 将 start.sh 和 purpur.jar 复制/下载到 /app 目录
COPY start.sh /app/start.sh
RUN curl -L -o /app/${PURPUR_JAR_NAME} "https://api.purpurmc.org/v2/purpur/${MC_VERSION}/latest/download"
RUN chmod +x /app/start.sh

# 3. 将工作目录设置为你指定的 /workspace
#    这意味着服务器启动后，所有生成的数据（world, plugins, eula.txt 等）都会在这个目录里
WORKDIR /workspace

# 4. 声明 /workspace 为数据卷，这是最佳实践
VOLUME /workspace

# --- 核心改动结束 ---

EXPOSE 25565

# 5. CMD 使用绝对路径执行 /app 中的脚本，这样就不会受 WORKDIR 影响
CMD ["/app/start.sh"]