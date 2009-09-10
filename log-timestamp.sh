# -*- mode:sh; coding:utf-8 -*-
while true; do
    echo logger: restarted at:`date -Is`..
    cat logger.fifo | while read line; do
        echo `ruby -e 't=Time.now; puts "#{t .strftime %q{%Y-%m-%d %H:%M:%S}}.#{t.usec.to_s[0..2]}"'`│ $line \
        >> `date -Im | cut -dT -f1 | cut -c3-`.log;
    done;
done & 