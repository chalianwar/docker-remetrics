package main


import (
	"github.com/heroku/docker-registry-client/registry"
	"github.com/heroku/docker-registry-client/vendor/github.com/docker/distribution/digest"
	"github.com/heroku/docker-registry-client/vendor/github.com/docker/distribution/manifest"
	"github.com/heroku/docker-registry-client/vendor/github.com/docker/libtrust"
	"fmt"
)

func main(){
	url      := "https://registry-1.docker.io/"
	username := "" // anonymous
	password := "" // anonymous
	hub, err := registry.New(url, username, password)
	if err != nil{
		//
	}
	repositories, err := hub.Repositories()
	fmt.Printf("%v\n", repositories)
	tags, err := hub.Tags("library/ubuntu")
	fmt.Printf("%v\n", tags)
	manifest, err := hub.Manifest("library/ubuntu", "1")
	fmt.Printf("%v\n", manifest)
	manifest1, err := hub.ManifestV2("library/ubuntu", "1")
	fmt.Printf("%v\n", manifest1)
}

