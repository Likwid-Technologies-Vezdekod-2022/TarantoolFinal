#!/usr/bin/env tarantool


local function init()
    meme = box.schema.space.create('meme')

    box.schema.sequence.create('autoincrement',{min=1, start=1})

    meme:format({
             {name = 'id', type = 'integer'},
             {name = 'original_image_path', type = 'string'},
             {name = 'generated_image_path', type = 'string'},
             {name = 'top_text', type = 'string'},
             {name = 'bottom_text', type = 'string'},
    })

    meme:create_index('primary', {
             type = 'hash',
             parts = {'id'},
             sequence='autoincrement'
             })
end


box.cfg{listen = 3301}
box.once('init', init)