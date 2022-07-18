FROM quay.io/centos/centos:stream9


RUN dnf install --enablerepo=crb -y gcc go nmstate-devel nmstate nmstate-libs && dnf clean all
# COPY --from=registry.ci.openshift.org/openshift/release:golang-1.17 /usr/local/go /usr/local/go

# ENV GOROOT=/usr/local/go
# ENV PATH=$PATH:$GOROOT/bin

WORKDIR /nmstate-experiments/

# Bring in the go dependencies before anything else so we can take
# advantage of caching these layers in future builds.
COPY main.go /nmstate-experiments/
COPY go.mod go.sum /nmstate-experiments/
RUN go mod download

COPY . /nmstate-experiments/

RUN CGO_ENABLED=1 GOFLAGS="" GO111MODULE=on go build -o /nmstate-experiments/main.go

#ARG WORK_DIR=/data

#RUN mkdir $WORK_DIR && chmod 775 $WORK_DIR
CMD ["ls", "/nmstate-experiments/"]

#CMD ["cat", "main.go"]
# CMD ["go", "run", "/nmstate-experiments/main.go"]