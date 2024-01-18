BEGIN {
  prev_total0 = 0
  prev_total1 = 0
  prev_idle0 = 0
  prev_idle1 = 0

  while (getline < "/proc/stat")
  {
    getline < "/proc/stat"
    idle0 = $5
    total0 = 0
    total1 = 0
    #print($1)
    for (i=2; i<=NF; i++)
      total0 += $i

    getline < "/proc/stat"
    close("/proc/stat")
    idle1 = $5
    #print($1)
    for (i=2; i<=NF; i++)
      total1 += $i

    percentage1 = (1-(idle0-prev_idle0)/(total0-prev_total0))*100
    percentage2 = (1-(idle1-prev_idle1)/(total1-prev_total1))*100
    print(percentage1+percentage2)

    prev_idle0 = idle0
    prev_total0 = total0
    prev_idle1 = idle1
    prev_total1 = total1
    system("sleep 5")
  }
}
