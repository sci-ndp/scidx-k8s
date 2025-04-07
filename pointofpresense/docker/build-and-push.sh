# Change 'yutianqin' to your own docker hub name 
# if you want to push the image to your own docker hub
docker buildx build --platform linux/amd64,linux/arm64 -t yutianqin/pop-api:latest --push --no-cache -f ./Dockerfile ..
