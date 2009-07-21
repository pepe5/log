# -*- ruby -*-
zzz = '...'

lambda {|lines| lines .each {|l| puts "#{l.chomp}:"; puts `#{l}` } } \
  .call <<-cmds
       echo #{zzz.chop!}
       echo #{zzz.chop!}
       echo #{zzz.chop!}
   cmds

def evalines lines; lines .each {|l| puts "#{l.chomp}:"; puts `#{l}` } ; end
# evalines <<-cmds
#     echo 1
#     echo 2
#     echo 3
# cmds

# rsync -av --exclude='.#*' /root/mnt/kraljo@jubiler/home/kraljo/small-projects/cr15282-20-digits/ ./
# git add .
# git diff HEAD | egrep '^\+' | egrep -v '^\+$' | head 
# git commit -a
