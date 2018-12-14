package main

import (
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}
func checkFileIsExist(filename string) bool {
	var exist = true
	if _, err := os.Stat(filename); os.IsNotExist(err) {
		exist = false
	}
	return exist
}
func main() {
	//fmt.Println(strings.Count(str, "id=")) // before & after each rune
	b, err := ioutil.ReadFile("aaa.txt") //chrome中拷贝数据到aaa.txt,https://www.jisilu.cn/data/stock/dividend_rate/#cn
	var filename = "./output1.txt"
	var f *os.File
	var err1 error
	if err != nil {
		fmt.Print(err)
	}
	if checkFileIsExist(filename) { //如果文件存在
		f, err1 = os.OpenFile(filename, os.O_APPEND, 0666) //打开文件
		fmt.Println("文件存在")
	} else {
		f, err1 = os.Create(filename) //创建文件
		fmt.Println("文件不存在")
	}
	check(err1)
	data := strings.Split(string(b), "id=")
	for i := 1; i < len(data); i++ {
		fmt.Println(data[i][1:7])
		io.WriteString(f, data[i][1:7]+"\r\n") //写入文件(字符串)

	}

}
