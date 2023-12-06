export interface GenerateHtmlRequest {
    requirements: string
}

export interface WebPage {
    id: string,
    in_processing: boolean,
    created_at: string,
    css: string,
    html: string,
    javascript: string,
    updated_at: string,
    url: string
}

export interface GenerateHtmlResponse {
    created_at: string,
    id: string,
    initial_requirements: string,
    web_pages: WebPage[]
}