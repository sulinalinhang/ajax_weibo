var apiWeiboAll = function(callback) {
    log('这是apiWeiboAll')
    var path = '/api/weibo/all'
    ajax('GET', path, '', callback)
//    r = ajax('GET', path, '', callback)
//    callback(r)
}

var apiWeiboAdd = function(form, callback) {
    var path = '/api/weibo/add'
    ajax('POST', path, form, callback)
}

var apiWeiboDelete = function(weibo_id, callback) {
    var path = `/api/weibo/delete?id=${weibo_id}`
    ajax('GET', path, '', callback)
}

var apiWeiboUpdate = function(form, callback) {
    var path = '/api/weibo/update'
    ajax('POST', path, form, callback)
}

var apiCommentAdd = function(form, callback) {
    var path = '/api/comment/add'
    ajax('POST', path, form, callback)
}

var apiCommentDelete = function(comment_id, callback) {
    var path = `/api/comment/delete?id=${comment_id}`
    ajax('GET', path, '', callback)
}

var apiCommentUpdate = function(form, callback) {
    var path = '/api/comment/update'
    ajax('POST', path, form, callback)
}

var weiboTemplate = function(weibo) {
// <span class="todo-id" hidden=True>${todo.id}</span>
    var w = `
        <span class="weibo-content">${weibo.content}</span>
        from
        <span class="weibo-userid">${weibo.username}</span>
        <button class="weibo-delete">删除</button>
        <button class="weibo-edit">编辑</button><br>
        <input class='input-comment'>
        <button class='comment-add'>发表评论</button><br>
    `
    return w
}

var commentTemplate = function(comment) {
    var c = `
        <div class="comment-cell" data-id="${comment.id}">
            <span class="comment-content" data-id="${comment.id}">${comment.content}</span>
            <button class="comment-delete" data-id="${comment.id}">删除</button>
            <button class="comment-edit">编辑</button><br>
        </div>
    `
    return c
}

var commentUpdateTemplate = function(content) {
    var c = `
        <div class="comment-update-form">
            <input class="comment-update-input" value="${content}">
            <button class="comment-update" >更新</button>
        </div>
    `
    return c
}

var weiboUpdateTemplate = function(content) {
    var w = `
        <div class="weibo-update-form">
            <input class="weibo-update-input" value="${content}">
            <button class="weibo-update" >更新</button>
        </div>
    `
    return w
}

var insertWeibo = function(weibo) {
    var weiboCell = weiboTemplate(weibo)
    var commentCell = ``
    log('这里', weibo['comments'] != undefined)
    if (weibo['comments'] != undefined) {
        for(var j = 0; j < weibo['comments'].length; j++) {
            commentCell += commentTemplate(weibo['comments'][j])
        }
    }
//    commentCell = `<div class="comment-cell">` + commentCell + `</div>`
    var all = `<div class="weibo-cell" data-id="${weibo.id}">` + weiboCell + commentCell + `</div><br>`
    // 插入 todo-list
    var weiboList = e('#id-weibo-list')
    weiboList.insertAdjacentHTML('beforeend', all)
}

var insertComment = function(comment) {
    var commentCell = commentTemplate(comment)
//    log('这是comment', commentCell)
//    var commentList = e('.comment-add', weiboCell)
    log('这是comment', commentCell, weiboCell)
    weiboCell.insertAdjacentHTML('beforeend', commentCell)
}

var insertUpdateForm = function(content, weiboCell) {
    var updateForm = weiboUpdateTemplate(content)
    weiboCell.insertAdjacentHTML('beforeend', updateForm)
}

var insertCommentUpdateForm = function(content, commentCell) {
    var updateForm = commentUpdateTemplate(content)
    commentCell.insertAdjacentHTML('beforeend', updateForm)
}

var loadWeibos = function() {
    // 调用 ajax api 来载入数据
    // todos = api_todo_all()
    // process_todos(todos)
    log('这是loadWeibos')
    apiWeiboAll(function(weibos) {
//        log('load all weibos', weibos)
        // 循环添加到页面中
        for(var i = 0; i < weibos.length; i++) {
            var weibo = weibos[i]
            log(weibo)
            insertWeibo(weibo)
//            for(var j = 0; j < weibos[i]['comments'].length; j++) {
//                insertComments(weibos[i]['comments'][j])
//            }
        }
    })
    // second call
}

var bindEventWeiboAdd = function() {
    var b = e('#id-button-add')
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function(){
        var input = e('#id-input-weibo')
        var content = input.value
        log('click add', content)
        var form = {
            content: content,
        }
        apiWeiboAdd(form, function(weibo) {
            // 收到返回的数据, 插入到页面中
            insertWeibo(weibo)
        })
    })
}


var bindEventWeiboDelete = function() {
    var todoList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    todoList.addEventListener('click', function(event) {
    log(event)
    // 我们可以通过 event.target 来得到被点击的对象
    var self = event.target
    log('被点击的元素', self)
    // 通过比较被点击元素的 class
    // 来判断元素是否是我们想要的
    // classList 属性保存了元素所有的 class
    log(self.classList)
    if (self.classList.contains('weibo-delete')) {
        log('点到了删除按钮')
        weiboId = self.parentElement.dataset['id']
        apiWeiboDelete(weiboId, function(r) {
            log('apiTodoDelete', r.message)
            // 删除 self 的父节点
            if (r.message.length == 4) {
                alert(r.message)
            } else {
                self.parentElement.remove()
                alert(r.message)
            }
        })
    } else {
        log('点到了 todo cell')
    }
})}

var bindEventWeiboEdit = function() {
    var weiboList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function(event) {
    log(event)
    // 我们可以通过 event.target 来得到被点击的对象
    var self = event.target
    log('被点击的元素', self)
    // 通过比较被点击元素的 class
    // 来判断元素是否是我们想要的
    // classList 属性保存了元素所有的 class
    log(self.classList)
    if (self.classList.contains('weibo-edit')) {
        log('点到了编辑按钮')
        weiboCell = self.closest('.weibo-cell')
        weiboId = weiboCell.dataset['id']
        var weiboSpan = e('.weibo-content', weiboCell)
        var content = weiboSpan.innerText
        // 插入编辑输入框
        insertUpdateForm(content, weiboCell)
    } else {
        log('点到了 todo cell')
    }
})}

var bindEventWeiboUpdate = function() {
    var weiboList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function(event) {
    log(event)
    // 我们可以通过 event.target 来得到被点击的对象
    var self = event.target
    log('被点击的元素', self)
    // 通过比较被点击元素的 class
    // 来判断元素是否是我们想要的
    // classList 属性保存了元素所有的 class
    log(self.classList)
    if (self.classList.contains('weibo-update')) {
        log('点到了更新按钮')
        weiboCell = self.closest('.weibo-cell')
        weiboId = weiboCell.dataset['id']
        log('update weibo id', weiboId)
        input = e('.weibo-update-input', weiboCell)
        content = input.value
        var form = {
            id: weiboId,
            content: content,
        }

        apiWeiboUpdate(form, function(weibo) {
            // 收到返回的数据, 插入到页面中
            log('apiWeiboUpdate', weibo)
            if (weibo.message == undefined) {
//                alert(weibo.message)
                var weiboSpan = e('.weibo-content', weiboCell)
                weiboSpan.innerText = weibo.content
            }else{
                alert(weibo.message)
//                var weiboSpan = e('.weibo-content', weiboCell)
//                weiboSpan.innerText = weibo.content
            }

            var updateForm = e('.weibo-update-form', weiboCell)
            updateForm.remove()
        })
    } else {
        log('点到了 todo cell')
    }
})}

var bindEventCommentAdd = function() {
    var weiboList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function(event) {
    log(event)
    // 我们可以通过 event.target 来得到被点击的对象
    var self = event.target
    log('被点击的元素', self)
    // 通过比较被点击元素的 class
    // 来判断元素是否是我们想要的
    // classList 属性保存了元素所有的 class
    log(self.classList)
    if (self.classList.contains('comment-add')) {
        log('点到了评论按钮')
        weiboCell = self.closest('.weibo-cell')
        weiboId = weiboCell.dataset['id']
        input = e('.input-comment', weiboCell)
        content = input.value
        log(content, weiboId)
        form = {
            content: content,
            weibo_id: weiboId,
        }
        apiCommentAdd(form, function(comment){
            log('QQQQQQ', weiboCell)
            insertComment(comment, weiboCell)
        })
//        var weiboInput = e('.input-comment', weiboCell)
//        var content = weiboSpan.innerText
        // 插入编辑输入框
//        insertUpdateForm(content, weiboCell)
    } else {
        log('点到了 todo cell')
    }
})}

var bindEventCommentDelete = function() {
    var todoList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    todoList.addEventListener('click', function(event) {
    log(event)
    // 我们可以通过 event.target 来得到被点击的对象
    var self = event.target
    log('被点击的元素', self)
    // 通过比较被点击元素的 class
    // 来判断元素是否是我们想要的
    // classList 属性保存了元素所有的 class
    log(self.classList)
    if (self.classList.contains('comment-delete')) {
        log('点到了删除按钮')
        commentId = self.dataset['id']
        apiCommentDelete(commentId, function(r) {
            log('apiCommentDelete', r.message)
            // 删除 self 的父节点
            if (r.message.length == 4) {
                alert(r.message)
//                self.parentElement.remove()
            }else{
                self.parentElement.remove()
                alert(r.message)
            }
        })
    } else {
        log('点到了 todo cell')
    }
})}

var bindEventCommentEdit = function() {
    var weiboList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function(event) {
    log(event)
    // 我们可以通过 event.target 来得到被点击的对象
    var self = event.target
    log('被点击的元素', self)
    // 通过比较被点击元素的 class
    // 来判断元素是否是我们想要的
    // classList 属性保存了元素所有的 class
    log(self.classList)
    if (self.classList.contains('comment-edit')) {
        log('点到了编辑按钮')
        commentCell = self.closest('.comment-cell')
        commentId = commentCell.dataset['id']
        var commentSpan = e('.comment-content', commentCell)
        var content = commentSpan.innerText
        // 插入编辑输入框
        insertCommentUpdateForm(content, commentCell)
    } else {
        log('点到了 todo cell')
    }
})}

var bindEventCommentUpdate = function() {
    var weiboList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function(event) {
    log(event)
    // 我们可以通过 event.target 来得到被点击的对象
    var self = event.target
    log('被点击的元素', self)
    // 通过比较被点击元素的 class
    // 来判断元素是否是我们想要的
    // classList 属性保存了元素所有的 class
    log(self.classList)
    if (self.classList.contains('comment-update')) {
        log('点到了更新按钮')
        commentCell = self.closest('.comment-cell')
        commentId = commentCell.dataset['id']
        log('update weibo id', commentId)
        input = e('.comment-update-input', commentCell)
        content = input.value
        var form = {
            id: commentId,
            content: content,
        }

        apiCommentUpdate(form, function(comment) {
            // 收到返回的数据, 插入到页面中
            log('apiWeiboUpdate', comment)
            if (comment.message == undefined) {
//                alert(comment.message)
                var commentSpan = e('.comment-content', commentCell)
                commentSpan.innerText = comment.content
            }else{
                alert(comment.message)
//                var commentSpan = e('.comment-content', commentCell)
//                commentSpan.innerText = comment.content
            }
            var updateForm = e('.comment-update-form', commentCell)
            updateForm.remove()
        })
    } else {
        log('点到了 todo cell')
    }
})}


var bindEvents = function() {
    bindEventWeiboAdd()
    bindEventWeiboDelete()
    bindEventWeiboEdit()
    bindEventWeiboUpdate()
    bindEventCommentAdd()
    bindEventCommentDelete()
    bindEventCommentEdit()
    bindEventCommentUpdate()
}

var __main = function() {
    bindEvents()
    loadWeibos()
}

__main()
