def breadthFiles p
  e = (Dir .new p) .entries
  e .select {|f| !File.directory?f} .each {|f| puts p+'/'+f}
  puts '---'
  e .select {|d| File.directory?d} .reject {|d| (d=~%r(\.$|\.\.$)) !=nil} .each {|d| breadth p+'/'+d} end
# breadthFiles '.'

def breadthDirs b, &f
  es = (Dir .new b) .entries
  # puts ">|"+b+": "+`echo $(ls -F #{b})`
  ps = es .map {|bs| b+'/'+bs} .select {|d| File.directory?d} .reject {|d| d .match %r(\.$|\.\.$)}
  # puts "ps: #{ps .join ' '}"
  ps .each {|d| f .call d}
  ps .each {|d| breadthDirs d,&f}
  # puts "<|"+b
end
breadthDirs ('.') {|d| puts `du -sh "#{d}"`}
