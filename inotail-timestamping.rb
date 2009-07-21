#!/usr/bin/ruby
def t; t = Time.now; "#{t .strftime '%Y-%m-%d %H:%M:%S'}.#{t.usec}" end
IO.popen "inotail -f #{ARGV[0]}" do |f| while line = f.gets; puts "#{t}|#{line}" end end
