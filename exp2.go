package main

import (
"fmt"
"github.com/nmstate/nmstate/rust/src/go/nmstate"
)

func main() {
//	hostYAML := `{
//"interfaces": [{
//  "name": "dummy1",
//  "state": "up",
//  "type": "dummy"
//}]}
//`
	hostYAML := `---
interfaces:
- name: dummy1
  state: up
  type: dummy
`
	nm := nmstate.New()
	stdout, err := nm.GenerateConfiguration(hostYAML)
	if err != nil {
		fmt.Println("ERROR:")
		fmt.Println(err.Error())
	}
	fmt.Println(stdout)
}

