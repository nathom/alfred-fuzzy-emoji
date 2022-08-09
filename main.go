package main

import (
	"encoding/json"
	"fmt"
	"github.com/reinhrst/fzf-lib"
	"os"
	"strings"
)

const MAXRESULTS = 20

type ReturnItem struct {
	Items []AlfredItem `json:"items"`
}

type IconItem struct {
	Path string `json:"path"`
}

type AlfredItem struct {
	Type     string   `json:"type"`
	Title    string   `json:"title"`
	Subtitle string   `json:"subtitle"`
	Icon     IconItem `json:"icon"`
	Arg      string   `json:"arg"`
}

func main() {
	if len(os.Args) < 2 {
		return
	}

	query := strings.Join(os.Args[1:], " ")

	var options = fzf.DefaultOptions()
	var myFzf = fzf.New(Descriptions, options)
	defer myFzf.End()
	var result fzf.SearchResult
	myFzf.Search(query)
	result = <-myFzf.GetResultChannel()
	maxResults := MAXRESULTS
	if len(result.Matches) < maxResults {
		maxResults = len(result.Matches)
	}

	results := make([]AlfredItem, 0, maxResults)
	for i := 0; i < maxResults; i++ {
		match := result.Matches[i]
		icon := fmt.Sprintf("/Users/nathan/alfred-fuzzy-emoji/images/%d.png", match.HayIndex)
		item := AlfredItem{
			Type:     "file",
			Title:    Titles[match.HayIndex] + " " + Emoji[match.HayIndex],
			Subtitle: fmt.Sprintf("Score: %d", match.Score),
			Icon: IconItem{
				Path: icon,
			},
			Arg: Emoji[match.HayIndex],
		}
		results = append(results, item)
	}

	if len(results) == 0 {
		results = []AlfredItem{
			{
				Type:     "file",
				Title:    "No results 😢",
				Subtitle: "Try searching again",
				Icon: IconItem{
					// 😵 image
					Path: "/Users/nathan/alfred-fuzzy-emoji/images/55.png",
				},
			},
		}
	}

	b, err := json.Marshal(ReturnItem{results})
	if err != nil {
		return
	}
	fmt.Print(string(b))
}
