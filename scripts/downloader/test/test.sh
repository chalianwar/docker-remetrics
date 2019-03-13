
go run down_loader.go -operation=download_manifest -repo=library/redis -tag=latest -absfilename=./test.manifest
go run down_loader.go -operation=download_blobs -repo=library/redis -tag=44888ef5307528d97578efd747ff6a5635facbcfe23c84e79159c0630daf16de  -absfilename=./test.tarball

