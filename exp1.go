//package nmstate_experiments

package main

import (
"fmt"
"github.com/nmstate/nmstate/rust/src/go/nmstate"
"sigs.k8s.io/yaml"
)

func main() {
	fmt.Println("Start")
	hostYAML := "dns-resolver:\n  config:\n    server:\n    - 192.168.126.1\ninterfaces:\n- ipv4:\n    address:\n    - ip: 192.168.126.30\n      prefix-length: 24\n    dhcp: false\n    enabled: true\n  name: eth0\n  state: up\n  type: ethernet\n- ipv4:\n    address:\n    - ip: 192.168.140.30\n      prefix-length: 24\n    dhcp: false\n    enabled: true\n  name: eth1\n  state: up\n  type: ethernet\nroutes:\n  config:\n  - destination: 0.0.0.0/0\n    next-hop-address: 192.168.126.1\n    next-hop-interface: eth0\n    table-id: 254\n"


	j2, err := yaml.YAMLToJSON([]byte(hostYAML))
	if err != nil {
		fmt.Printf("err: %v\n", err)
	}
	fmt.Println(string(j2))

	//hostYAML := " <dns-resolver:\n  config:\n    server:\n    - 192.168.126.1\ninterfaces:\n- ipv4:\n    address:\n    - ip: 192.168.126.30\n      prefix-length: 24\n    dhcp: false\n    enabled: true\n  name: eth0\n  state: up\n  type: ethernet\n- ipv4:\n    address:\n    - ip: 192.168.140.30\n      prefix-length: 24\n    dhcp: false\n    enabled: true\n  name: eth1\n  state: up\n  type: ethernet\nroutes:\n  config:\n  - destination: 0.0.0.0/0\n    next-hop-address: 192.168.126.1\n    next-hop-interface: eth0\n    table-id: 254\n>"
//	hostYAML := `'---
//interfaces:
//- name: bond99
//  type: bond
//  state: up
//  link-aggregation:
//    mode: balance-rr
//    port:
//    - eth2'`
//
//	hostYAML := `{
//"interfaces": [{
//  "name": "dummy1",
//  "state": "up",
//  "type": "dummy"
//}]}
//`
//	hostYAML := `---
//interfaces:
//- name: dummy1
//  state: up
//  type: dummy
//`
	nm := nmstate.New()
	stdout, err := nm.GenerateConfiguration(string(j2))
	if err != nil {
		fmt.Println("ERROR:")
		fmt.Println(err.Error())
	}
	fmt.Println(stdout)
	fmt.Println("end")
}

