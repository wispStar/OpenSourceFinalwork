from sys import settrace, gettrace
import linecache
import pkg_resources

proj_prefix = pkg_resources.get_distribution('holidays').location + '\\holidays\\'
f = open('trace_record_import.txt', 'w+', encoding='utf-8')


def tracer(frame, event, arg):
    old = gettrace()
    settrace(None)
    if event == 'call':
        filename = frame.f_code.co_filename.lower()
        if filename.startswith(proj_prefix):
            # if True:
            lineno = frame.f_lineno
            func = frame.f_code.co_name
            filename = filename.replace(proj_prefix, '')
            f.write(f'(call) {filename}:{lineno}: {func}\n')

    if event == 'line':
        filename = frame.f_code.co_filename.lower()
        # if filename != last_filename and filename.startswith(proj_prefix):
        if filename.startswith(proj_prefix):
            # if True:
            line_no = frame.f_lineno
            line = linecache.getline(filename, line_no).strip()
            filename = filename.replace(proj_prefix, '')
            f.write(f'\t{filename}:{line_no}: {line}\n')
    settrace(old)
    return tracer


settrace(tracer)
import holidays

f = open('trace_record_call.txt', 'w+', encoding='utf-8')
holidays.CN()['2023-04-05']  # 清明节
