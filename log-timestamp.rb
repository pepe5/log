#!/usr/bin/ruby
# -*- mode:ruby; coding:utf-8 -*-
##
# TODO:
# of >! //stackoverflow.com/questions/972370/how-do-you-pipe-input-through-grep-to-another-utility #: tail -f 1.log | while read line ; do echo "$line"; done
# or >? may be PTY? //objectmix.com/java/75931-how-read-unbuffered-stdout-new-process.html

STDOUT.sync = true
puts "argv:#{ARGV}, -size:#{ARGV.size}" if $DEBUG
def t; t = Time.now; "#{t .strftime %q{%Y-%m-%d %H:%M:%S}}.#{t.usec.to_s[0..2]}" end
IO.popen "inotail -f #{ARGV[0]}" do |f| while line = f.gets; puts "#{t}│#{line}" end end if ARGV.size>0
$stderr .puts "#{$0}: <&1"
while line = gets; puts "#{t}│#{line}" end

##
# USE:
# mkfifo logger.fifo
# cat logger.fifo | ruby ../log-timestamp.rb | while read line; do echo $line | cat -t; done & # for UI; OR:
# while true; do echo logger: restarting at: `date -Is`; cat logger.fifo | ruby ~/text/log/log-timestamp.rb >> `date -Im | cut -dT -f1 | cut -c3-`.log; done & # for back-end
# script -f logger.fifo
# dtach -A session.dtach -z bash


# old stu:
# NY fix from: //www.unix.com/unix-dummies-questions-answers/23590-getting-time-mili-seconds.html
# > cat 1.fifo | while read line; do echo $(date +'%F %l:%M:%S').$(( $(date +%N) / 100000 ))│ $line; done | cat
# < bash: 029351000: value too great for base (error token is "029351000")


# $Id: inotail-t.rb,v 1.6 2009/09/03 19:52:26 root Exp $
