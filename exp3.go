package main

import (
	"context"
	"fmt"
	"sync"
	//"time"

	"github.com/pkg/errors"
	"github.com/sirupsen/logrus"
	"golang.org/x/sync/semaphore"
)


func generateHostStaticNetworkConfigData (hostname string) ([]string, error){
	//if hostname == "host2" {
	//	return nil, errors.New("host2 error!")
	//}

	file1 := fmt.Sprintf("%s.file1 ", hostname)
	file2 := fmt.Sprintf("%s.file2 ", hostname)
	file3 := fmt.Sprintf("%s.file3 ", hostname)

	return []string{file1, file2, file3}, nil

}

func test() error {
	var (
		globalErr error
		wg sync.WaitGroup
		filesList []string

	)

	sem := semaphore.NewWeighted(20)

	for i := 1; i <=10; i++ {
		if lockErr := sem.Acquire(context.Background(), 1) ; lockErr != nil{
			logrus.WithError(lockErr).Errorf("Failed to lock semaphore for execution")
			return lockErr
		}
		logrus.Infof("XXXXX: iteration %d GOT LOCK!", i)

		wg.Add(1)
		go func(x int) {
			defer wg.Done()
			//if x == 4 {
			//time.Sleep(1 * time.Second)
			//}
			logrus.Infof("XXXXX: starting go fun for: %d", x)

			hostFileList, routineErr := generateHostStaticNetworkConfigData(fmt.Sprintf("host%d", x))
			if routineErr != nil {
				routineErr = errors.Wrapf(routineErr, "failed to create static config for host %d", x)
				logrus.Error(routineErr)
				globalErr = routineErr
				return
			}

			filesList = append(filesList, hostFileList...)

		}(i)

		sem.Release(1)
		logrus.Infof("XXXXX: iteration %d RELEASED LOCK!", i)

	}
	wg.Wait()
	logrus.Info("XXXXX: Done waiting!")
	// if any of the go routines return an error
	if globalErr != nil {
		return globalErr
	}
	//for f :=  range filesList {
	//	fmt.Print(f)
	//}

	//logrus.Info(filesList)
	return nil
}


func main() {

	logrus.Println("start")

	if err := test() ; err != nil{
		logrus.Println(err.Error())
	}

	logrus.Println("end")
}
