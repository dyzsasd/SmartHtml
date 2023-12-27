export interface GenerateHtmlRequest {
    requirements: string
}

export interface WebPage {
    _id: string,
    in_processing: boolean,
    created_at: string,
    css: string,
    html: string,
    javascript: string,
    updated_at: string,
    url: string,
    comments: {
        element_comments: string[],
        global_comment: {
            __type: string,
            text: string
        }
    }
}

export interface Session {
    created_at: string,
    _id: string,
    initial_requirements: string,
    web_pages: WebPage[]
}