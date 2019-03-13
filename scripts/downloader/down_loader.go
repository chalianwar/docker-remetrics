package main


import (
	"github.com/heroku/docker-registry-client/registry"
	"github.com/docker/distribution/digest"
	//manifestV2 "github.com/docker/distribution/manifest/schema2"
	//"github.com/docker/distribution/manifest"
	//"github.com/docker/libtrust"
	"fmt"
	//"C"
	//"io"
	//"net/http"
	"io/ioutil"
	"bytes"
	"io"
	"os"
	"flag"
	"net/http"
	"strings"
	"time"
)
/* TODO
	1. add log file
	2. fix the parameter names' more readable
	3. catch exceptions (input, timeout)
*/

func registry_init() (*registry.Registry, error){
	url      := "https://registry-1.docker.io/"
	username := "" // anonymous
	password := "" // anonymous
	hub, err := registry.New(url, username, password)
	if err != nil{
		registry.Log("###########cannot init a regisrty!############")
		return nil, err
	}
	//repositories, err := hub.Repositories()
	return hub, nil
}

func docker_download(input_op string, input_repo string, input_tag string, output_filename string) error {
	hub, err := registry_init()
	if err != nil{
		registry.Log("###########Error, cannot download anything!############")
		return err
	}

	repo_name := input_repo
	repo_op := input_op
	repo_tag := input_tag
	absfilename := output_filename

	switch repo_op {
	case "download_blobs":
		registry.Log("download blobs!")
		err := get_blobs(hub, repo_name, repo_tag, absfilename)
		return err
	case "download_manifest":
		registry.Log("download manifest!")
		err := get_manifest(hub, repo_name, repo_tag, absfilename)
		return err
		//printResponse(manifest)
	}
	return nil
}

func get_manifest(hub *registry.Registry, repo_name string, repo_tag string, absfilename string) error {
	//fmt.Printf("%v\n", repositories)
	//tags, err := hub.Tags("library/ubuntu")
	//fmt.Printf("%v\n", tags)
	//manifest, err := hub.Manifest("library/ubuntu", "1")
	//fmt.Printf("%v\n", manifest)
	registry.Log("start get manifest")
	manifest2, err := hub.ManifestV2(repo_name, repo_tag)
	if err != nil{
		registry.Log("Fail to get manifest: Failed repo: %v\n, error message: %s", repo_name,			err)
		return err
	}
	//fmt.Printf("%v\n", manifest2)
	//printResponse(manifest2)
	err = storeBlob(absfilename, manifest2.Body)
	if err != nil{
		return err
	}
	defer manifest2.Body.Close()

	return nil
}

func get_blobs(hub *registry.Registry, repo_name string, blob_digest string, absfilename string) error {
	digest := digest.NewDigestFromHex(
		"sha256",
		blob_digest,
	)
	reader, err := hub.DownloadLayer(repo_name, digest)
	if reader != nil {
		//registry.Log("Cannot download blobs: %v", blob_digest)
		defer reader.Close()
	}
	if err != nil {
		registry.Log("Cannot download blobs: %v", blob_digest)
		return err
	}

	err = storeBlob(absfilename, reader)
	//defer reader.Close()
	return err
}

func printResponse(resp *http.Response) error {
	var response []string

	bs, err := ioutil.ReadAll(resp.Body)
	if err != nil{
		registry.Log("Fail to read resp.body!")
		return err
	}
	rdr1 := ioutil.NopCloser(bytes.NewBuffer(bs))
	rdr2 := ioutil.NopCloser(bytes.NewBuffer(bs))
	//doStuff(rdr1)
	resp.Body = rdr2

	buf1 := new(bytes.Buffer)
	buf1.ReadFrom(rdr1)
	tr := buf1.String()

	//tr := string(rdr1)
	//buf1 := new(bytes.Buffer)
	//buf1.ReadFrom(resp.Body)
	//bs1 := buf1.String()

	response = append(response, fmt.Sprintf("%v", tr))

	//// Loop through headers
	//for name, headers := range resp.Header {
	//	name = strings.ToLower(name)
	//	for _, h := range headers {
	//		response = append(response, fmt.Sprintf("%v: %v", name, h))
	//	}
	//}

	//logrus.Debugf("PingV2Registry: http.NewRequest: GET %s body:nil", endpointStr)

	strings.Join(response, "\n")
	registry.Log("<manifest>%s<manifest>\n", response)
	return nil
}

func storeBlob(absFileName string, resp io.ReadCloser) error {

	registry.Log("start storeBlob")

	//bs, err := ioutil.ReadAll(resp)
	//if err != nil{
	//	//return nil
	//}
	//rdr1 := ioutil.NopCloser(bytes.NewBuffer(bs))
	//rdr2 := ioutil.NopCloser(bytes.NewBuffer(bs))
	//resp = rdr2
	//
	//buf1 := new(bytes.Buffer)
	//buf1.ReadFrom(rdr1)
	//
	//err = ioutil.WriteFile(absFileName, buf1.Bytes(), 0644)
	//if err != nil {
	//	//err handling
	//}
	/*
	Given an io.ReadCloser, from the response of an HTTP request for example,
	what is the most efficient way both in memory overhead and code readability
	to stream the response to a File?
	*/
	start := time.Now().UnixNano()
	outFile, err := os.Create(absFileName)
	if err != nil{
		registry.Log("Fail to create a file for the blob: %v", absFileName)
		return err
	}
	defer  outFile.Close()
	size, err := io.Copy(outFile, resp)
	if err != nil{
		registry.Log("Fail to copy the resp to outFile %v!", absFileName)
		return err
	}
	end := time.Now().UnixNano()
	elapsed := float64((end - start) / 1000) //millisecond
	registry.Log("finished storeBlob time: ====> (%v MB / %v s) %v MB/s", float64(size) / 1024 / 1024,
		float64(elapsed) / 1000000,
		float64(size) / float64(elapsed))
	return nil
}

func main() {

	input_op := flag.String("operation", "download_blobs", "download_blobs or download_manifest")
	input_repo := flag.String("repo", "library/redis", "image'name including namespace/reponame")
	filename := flag.String("absfilename", "./test", "The output filename: tarball filename or manifest name")
	input_tag := flag.String("tag", "latest", "repo tag or layer digest")
	//input_op string, input_repo string, input_tag string, output_filename string
	//go run down_loader.go -operation=download_manifest -repo=library/redis -tag=latest -absfilename=./test
	flag.Parse()
	fmt.Println("repo name:", *input_repo)
	fmt.Println("output filename:", *filename)
	fmt.Println("operation:", *input_op)
	fmt.Println("tag:", *input_tag)

	err := docker_download(*input_op, *input_repo, *input_tag, *filename)
	if err != nil{
		registry.Log("############ Main: No file is downloaded! #############")
	}
}


