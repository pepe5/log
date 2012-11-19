# % catch {close $h}; set h [open $InLogs]; source sc.tcl
# % getl -cache cache $h
# % getl -cache cache $h
# % getl -cache cache $h
set InLogs {.sc/try,5.log}
set StarteRE {^([0-9][0-9][:.][0-9][0-9][:.][0-9][0-9][:.][0-9]+)\|}

proc getl {{ch stdin} {ov ov} {cachek -cache} {cachev cachev}} \
  { global StarteRE
    upvar $cachev cache
    # set ch [if {[llength $args]} {lindex $args 0}] ;#{stdin}
    # puts "cachev:$cachev, cache:$cache, ch:$ch, ov:$ov"
    set cn [string length $cache]
    set n [if {!$cn} {gets $ch cache} {set - 0}] ;#>? set - $cn
    puts ">| $n: $cache"
    set log "" ;# list
    lappend log $cache
    if {$ov != "ov"} { upvar $ov o }
    set o ""
   
    while {1} \
      { set cn [gets $ch cache]
        if {0>$cn} break
        set mn [regexp "$StarteRE" "$cache" m t]
        puts "[if {$mn} {set - x} {set - +}]> $cn: $cache"
        if {!$mn} {lappend log $cache; set n $cn} \
          else break }
    set o [join $log "\n"]
    return [if {$ov != "ov"} {set - $n} {set - $o}] }

# return 1

set colsRE {([0-9:.]+)\| ([a-z]+) \"([^"]+)\"\| ([^|]+)\|(.*)} ;#" ([a-z0-9/_]+)
set p /dev/null
set l ""

set cacheDir [glob .sc]
puts "cache: $cacheDir/"
if {[llength $cacheDir]} {puts "- here we can.."} {exit 1}
        
exec rm -rf .sc/kraljo
catch {close $ih}; set ih [open $InLogs]
# fconfigure $ih -blocking ;#?<
set cache ""

while {1} \
  { set n [getl $ih l -cache cache]
    puts "<| l:$l"
      if {0>$n} break ;# !< use tail-f -able construct :-|
      set n [regexp $colsRE "$l" - t c p opt v] ;# (t)ime (c)ommand (p)ath meta-data-(opt)ions (v)alue-tail
    if {! $n} \
      { puts "(nothing rec/d)"
        set h [open .sc/.unlocated a+]
        puts "(adding change > unlocated: $l)"
        foreach e [split $l "\n"] {puts $h $l} ;#?< isnt there "read" opossite?
        close $h } \
      else \
      { puts "t:$t, c:$c, p:$p, v:$v|"
        catch {set n [exec egrep -n $StarteRE $InLogs]} ;#>! | tail -1 | cut -d: -f1 ..
        set tail1 [lindex [split $n "\n"] end]
        set n [string range "$tail1" 0 [expr [string first : "$tail1"]-1]]
        puts " (#n:$n)"

        regexp {(.*)/(.*)} $p - d f
        puts "d:$d f:$f"
        set cmd "mkdir -v -p .sc/$d"; puts "$cmd #.."; catch {eval [concat exec $cmd]}
        
        switch $c \
          { add \
		{  puts " > add"
		    set h [open .sc/$p a]
		    puts "adding value > $p: $v"
		    foreach e [split $v "\n"] {puts $h $e} ;#?< isnt there "read" opossite?
		    close $h }
            patch {puts " > patch.."}
            default \
		{  puts " >| set:"
		    set h [open .sc/$p w]
		    puts "setting value > $p: $v"
		    foreach e [split $v "\n"] {puts $h $e} ;#?< isnt there "read" opossite?
		    close $h } }

        #>! set cmd "echo $l >> .sc/$p"; puts "$cmd #.."; eval [concat exec $cmd]
        set h [open .sc/$p.sc a+]
        puts "adding change > $p.sc: $l"
        foreach e [split $l "\n"] {puts $h $e}
        close $h
        
        # set cmd "cat -vns .sc/$p"; puts "$cmd #.."; eval [concat exec $cmd] ;#? in v3 NOk?
      } }
