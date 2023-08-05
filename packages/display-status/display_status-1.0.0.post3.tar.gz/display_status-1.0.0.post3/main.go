package main

import "C"

import (
	"fmt"
	"io"
	"net/http"
	"net/url"
	"sync"

	"github.com/fatih/color"
	"golang.org/x/net/html"
	"golang.org/x/net/proxy"
)

var (
	mtx = sync.Mutex{}
)

func getTitle(body io.ReadCloser) string {
	tokenizer := html.NewTokenizer(body)
	for {
		tokenType := tokenizer.Next()
		switch tokenType {
		case html.ErrorToken:
			return ""
		case html.StartTagToken:
			name, _ := tokenizer.TagName()
			if string(name) == "title" {
				tokenizer.Next()
				return string(tokenizer.Text())
			}
		}

	}
}

func isValidURL(link string) bool {
	uri, err := url.Parse(link)
	return err == nil && (uri.Scheme == "http" || uri.Scheme == "https")
}

func formatResponse(response *http.Response) string {
	return fmt.Sprintf("%d %s", response.StatusCode, getTitle(response.Body))
}

//export DisplayLinks
func DisplayLinks(links []string) int {
	socksProxy, err := proxy.SOCKS5("tcp", "127.0.0.1:9050", nil, proxy.Direct)
	if err != nil {
		fmt.Printf("Unable to connect to proxy. Error: %+v", err)
		return 1
	}
	tr := &http.Transport{Dial: socksProxy.Dial}
	client := &http.Client{
		Transport: tr,
	}
	mtx.Lock()
	defer mtx.Unlock()
	for _, link := range links {
		if !isValidURL(link) {
			color.Red("%d %s", http.StatusNotFound, link)
			continue
		}
		response, err := client.Get(link)
		if err != nil || response.StatusCode > 300 {
			color.Red("%d %s", response.StatusCode, link)
		} else {
			color.Green(formatResponse(response))
		}
		response.Body.Close()
	}
	return 0
}

func main() {}
