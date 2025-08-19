docker service create \
    --name dokploy-postgres \
    --constraint 'node.role==manager' \
    --network dokploy-network \
    --env POSTGRES_USER=dokploy \
    --env POSTGRES_DB=dokploy \
    --env POSTGRES_PASSWORD=amukds4wi9001583845717ad2 \
    --mount type=volume,source=dokploy-postgres-database,target=/var/lib/postgresql/data \
    postgres:16
 
docker service create \
    --name dokploy-redis \
    --constraint 'node.role==manager' \
    --network dokploy-network \
    --mount type=volume,source=redis-data-volume,target=/data \
    redis:7


docker service create \
      --name dokploy \
      --replicas 1 \
      --network dokploy-network \
      --mount type=bind,source=/var/run/docker.sock,target=/var/run/docker.sock \
      --mount type=bind,source=/volume1/docker/dokploy/dokploy,target=/etc/dokploy \
      --mount type=volume,source=dokploy-docker-config,target=/root/.docker \
      --publish published=13000,target=3000,mode=host \
      --update-parallelism 1 \
      --update-order stop-first \
      --constraint 'node.role == manager' \
      -e ADVERTISE_ADDR=192.168.50.252 \
      dokploy/dokploy:latest


docker service create \
      --name dokploy-traefik \
      --constraint 'node.role==manager' \
      --network dokploy-network \
      --mount type=bind,source=/volume1/docker/dokploy/traefik/traefik.yml,target=/etc/traefik/traefik.yml \
      --mount type=bind,source=/volume1/docker/dokploy/dokploy/traefik/dynamic,target=/etc/dokploy/traefik/dynamic \
      --mount type=bind,source=/var/run/docker.sock,target=/var/run/docker.sock \
      --publish mode=host,published=10443,target=443 \
      --publish mode=host,published=10080,target=80 \
      --publish mode=host,published=10443,target=443,protocol=udp \
      traefik:v3.1.2