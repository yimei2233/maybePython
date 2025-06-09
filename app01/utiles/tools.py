from django.utils.safestring import mark_safe




# 分页处理
# 参数1：当前页数
# 参数2：总条数
# 参数3：每页显示条数

def handle_page(page, total_count, page_size, **dt):

    # 参数处理
    args = ''
    for key,value in dt.items():
        args += '&'+str(key)+'='+str(value)

    total_page_count, div = divmod(total_count, page_size)
    if div:
        total_page_count += 1

    # 极值页码处理
    plus = 5
    if total_page_count <= 2 * plus + 1:
        start_page = 1
        end_page = total_page_count
    else:
        if page <= plus:
            start_page = 1
            end_page = 2 * plus + 1
        else:
            if (page + plus) > total_page_count:
                start_page = total_page_count - 2 * plus
                end_page = total_page_count
            else:
                start_page = page - plus
                end_page = page + plus

    page_str_list = []

    # 首页
    page_str_list.append('<li><a href="?page=1'+args+'">首页</a></li>')

    # 上一页
    if page > 1:
        prev = '<li><a href="?page='+str(page-1)+args+'" aria-label="Previous"><span aria-hidden="true">上一页</span></a></li>'
    else:
        prev = '<li><a href="?page=1'+args+'" aria-label="Previous"><span aria-hidden="true">上一页</span></a></li>'
    page_str_list.append(prev)

    # 页码
    for i in range(start_page, end_page + 1):
        if i == page:
            ele = '<li class="active" style="background-color:#086C9D;"><a href="?page='+str(i)+args+'" style="color:white;">'+str(i)+'</a></li>'
        else:
            ele = '<li><a href="?page='+str(i)+args+'">'+str(i)+'</a></li>'
        page_str_list.append(ele)

    # 下一页
    if page < total_page_count:
        nt = '<li><a href="?page='+str(page+1)+args+'" aria-label="Previous"><span aria-hidden="true">下一页</span></a></li>'
    else:
        nt = '<li><a href="?page='+str(total_page_count)+args+'" aria-label="Previous"><span aria-hidden="true">下一页</span></a></li>'
    page_str_list.append(nt)

    # 尾页
    page_str_list.append('<li><a href="?page='+str(total_page_count)+args+'">尾页</a></li>')
    page_string = mark_safe(''.join(page_str_list))
    return page_string
