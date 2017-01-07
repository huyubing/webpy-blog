#coding=utf-8
""" Basic blog using webpy 0.3 """

### 中文

import web
import model

### Url mappings

urls = (
    '/', 'Index',
    '/view/(\d+)', 'View',
    '/new', 'New',
    '/delete/(\d+)', 'Delete',
    '/edit/(\d+)', 'Edit',
    '/svn', 'Svn'    # svn管理页面
)


### Templates
t_globals = {
    'datestr': web.datestr
}
render = web.template.render('templates', base='base', globals=t_globals)


class Index:

    def GET(self):
        """ Show page """
        posts = model.get_posts()
        return render.index(posts)


class View:

    def GET(self, id):
        """ View single post """
        post = model.get_post(int(id))
        return render.view(post)


class New:

    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull, 
            size=30,
            description=u"标题:"),
        web.form.Textarea('content', web.form.notnull, 
            rows=30, cols=80,
            description=u"内容:"),
        web.form.Button('OK'),
        web.form.Button("submit", type="submit", description="Register"),
    )

    def GET(self):
        print "New:GET"
        form = self.form()
        return render.new(form)

    def POST(self):
        print "New:POST"
        form = self.form()
        if not form.validates():
            return render.new(form)
        print "Post2"
        print form.d.title
        print form.d.content
        model.new_post(form.d.title, form.d.content)
        raise web.seeother('/')


class Delete:

    def GET(self, id):
        model.del_post(int(id))
        raise web.seeother('/')

    def POST(self, id):
        model.del_post(int(id))
        raise web.seeother('/')


class Edit:

    def GET(self, id):
        print "id" + id
        post = model.get_post(int(id))
        form = New.form()
        form.fill(post)
        return render.edit(post, form)


    def POST(self, id):
        form = New.form()
        post = model.get_post(int(id))
        if not form.validates():
            return render.edit(post, form)
        model.update_post(int(id), form.d.title, form.d.content)
        raise web.seeother('/')


class Svn:
    
    def GET(self):
        lists = model.get_svn_list()
        return render.svn(lists)
        
app = web.application(urls, globals())

if __name__ == '__main__':
    print "start"
    app.run()
