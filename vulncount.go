package main

import (
    "fmt"
    "bufio"
    "os"
    "log"
    "strings"
    "strconv"
)

func isVulnerable(minor int, release int) bool {
    switch minor {
    case 1:
    case 2:
    case 3:
    case 4:
        if release < 17 {
            return true
        }
    case 13:
        if release < 7 {
            return true
        }
    case 14:
        if release < 3 {
            return true
        }
    case 15:
        if release < 2 {
            return true
        }
    case 16:
        if release < 4 {
            return true
        }
    case 17:
        if release < 4 {
            return true
        }
    case 18:
        if release < 1 {
            return true
        }
    default:
        return false
    }
    return false
}

func main() {
    count := 0
    handle, e := os.Open(os.Args[1])
    if e != nil {
        log.Fatal(e)
    }
    scanner := bufio.NewScanner(handle)
    for scanner.Scan() {
        versionNumber := strings.TrimPrefix(scanner.Text(), "    Confluence version no: ")
        versionFields := strings.Split(versionNumber, ".")
        if versionFields[0] == "6" {
            count++
            fmt.Println(versionNumber)
            continue
        }
        if versionFields[0] == "7" {
            minor, e := strconv.Atoi(versionFields[1])
            if e != nil {
                log.Fatal(e)
            }
            release, e := strconv.Atoi(versionFields[2])
            if e != nil {
                log.Fatal(e)
            }
            if isVulnerable(minor, release) { 
                fmt.Println(versionNumber)
                count++
                continue
            }
        }
    }
    fmt.Printf("%d versions vulnerable to CVE 2022-26134 in this scan\n", count)
}
