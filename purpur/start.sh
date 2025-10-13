#!/bin/sh

# 自动同意 Minecraft EULA
echo "eula=true" > eula.txt

# 设置默认内存，如果环境变量 MEMORY 未设置，则使用 4G
MEMORY=${MEMORY:-4G}

# 使用 Aikar's Flags 优化启动参数
# exec 会让 Java 进程替换掉 shell 进程，成为容器的主进程 (PID 1)，这样可以更好地接收 Docker 的停止信号
exec java -Xms${MEMORY} -Xmx${MEMORY} \
    -XX:+UseG1GC \
    -XX:+ParallelRefProcEnabled \
    -XX:MaxGCPauseMillis=200 \
    -XX:+UnlockExperimentalVMOptions \
    -XX:+DisableExplicitGC \
    -XX:+AlwaysPreTouch \
    -XX:G1NewSizePercent=30 \
    -XX:G1MaxNewSizePercent=40 \
    -XX:G1HeapRegionSize=8M \
    -XX:G1ReservePercent=20 \
    -XX:G1HeapWastePercent=5 \
    -XX:G1MixedGCCountTarget=4 \
    -XX:InitiatingHeapOccupancyPercent=15 \
    -XX:G1MixedGCLiveThresholdPercent=90 \
    -XX:G1RSetUpdatingPauseTimePercent=5 \
    -XX:SurvivorRatio=32 \
    -XX:+PerfDisableSharedMem \
    -XX:MaxTenuringThreshold=1 \
    -Dusing.aikars.flags=https://mcflags.emc.gs \
    -Daikars.new.flags=true \
    -jar purpur.jar --nogui