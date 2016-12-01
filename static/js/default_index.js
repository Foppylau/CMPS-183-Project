// This is the js for the default/index.html view.

var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };

    function get_posts_url(start_idx, end_idx) {
        var pp = {
            start_idx: start_idx,
            end_idx: end_idx
        };
        return posts_url + "?" + $.param(pp);
    }

    self.get_posts = function () {
        $.getJSON(get_posts_url(0, 4), function (data) {
            self.vue.posts = data.posts;
            self.vue.has_more = data.has_more;
            self.vue.logged_in = data.logged_in;
        });
    };

    self.get_more = function () {
        var num_posts = self.vue.posts.length;
        $.getJSON(get_posts_url(num_posts, num_posts + 4), function (data) {
            self.vue.has_more = data.has_more;
            self.extend(self.vue.posts, data.posts);
        });
    };

    self.add_post_button = function () {
        // The button to add a post has been pressed.
        self.vue.is_adding_post = !self.vue.is_adding_post;
    };

    self.add_post = function () {
        // The submit button to add a post has been added.

            $.post(add_post_url,
                {
                    post_content: self.vue.form_content,
                    circle: self.vue.form_circle,
                    price: self.vue.form_price,
                    status: self.vue.form_status
                },
                function (data) {
                    $.web2py.enableElement($("#add_post_submit"));
                    self.vue.posts.unshift(data.post);
                });

    };

    self.delete_post = function(post_id) {
        $.post(del_post_url,
            {
                post_id: post_id
            },
            function () {
                var idx = null;
                for (var i = 0; i < self.vue.posts.length; i++) {
                    if (self.vue.posts[i].id === post_id) {
                        // If I set this to i, it won't work, as the if below will
                        // return false for items in first position.
                        idx = i + 1;
                        break;
                    }
                }
                if (idx) {
                    self.vue.posts.splice(idx - 1, 1);
                }
            }
        )
    };



    self.add_picture_button = function () {
        self.vue.is_adding_picture = !self.vue.is_adding_picture;
    };

    self.edit_post = function(post_idx){
        var post = self.vue.posts[post_idx];
        self.vue.selected_idx = post_idx;
        self.vue.edited_content = post.content;
        self.vue.is_adding_post = false;
    };

    self.update_post = function (post_idx) {
       $.post(edit_post_url,
           {
               post_id: self.vue.posts[post_idx].id,
               edit_content: self.vue.edited_content
           },
           function (data) {
               //hides the edit form after post has been updated
               if(!data.idx)
                   self.vue.selected_idx = null;
                self.get_posts();
           });
    };




    self.add_item_button = function() {
        self.vue.is_adding_item = !self.vue.is_adding_item;

    };

    self.add_item = function(post_idx) {
        $.post(add_item_url,
            {
                item_name: self.vue.form_item_name,
                bill_name: self.vue.posts[post_idx].content,
            },
            function (data) {
                if(!data.idx)
                    self.vue.selected_idx = null;
                self.get_posts();
                $.web2py.enableElement($("#add_item_submit"));
            });
    };

    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            is_adding_post: false,
            is_adding_picture: false,
            is_editing_post: false,
            is_adding_item: false,
            posts: [],
            items: [],
            logged_in: false,
            has_more: false,
            selected_idx: null,
            edited_content: null,
            form_content: null,
            edit_content: null,
            form_circle: null,
            form_price: null,
            form_status: null,
            form_item_name: null,
            form_item_price: null
        },
        methods: {
            get_more: self.get_more,
            add_post_button: self.add_post_button,
            add_picture_button: self.add_picture_button,
            edit_post_button: self.edit_post_button,
            add_post: self.add_post,
            edit_post: self.edit_post,
            delete_post: self.delete_post,
            add_item_button: self.add_item_button,
            add_item: self.add_item

        },

        filters: {
            reverse: function (data) {
                return data.reverse()
            }
        }
    });

    self.get_posts();
    $("#vue-div").show();


    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});