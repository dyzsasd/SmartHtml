import request from "./request";

import {
    GenerateHtmlRequest, Session, WebPage
} from "./model"

export const generateHtml = async (requestModel: GenerateHtmlRequest): Promise<Session> => {
    return request.post<Session>('/session', requestModel);
};

export const getSession = async (sessionId: string): Promise<Session> => {
    return request.get<Session>(`/session/${sessionId}`);
};

export const comments = async (sessionId: string, webpageId: string, global: string, element_comments: {}): Promise<Session> => {
    return request.put<Session>(`/session/${sessionId}/webpage/${webpageId}/comments`, {
        global: global,
        element_comments: element_comments
    });
}

export const update = async (sessionId: string, webpageId: string): Promise<WebPage> => {
    return request.put<WebPage>(`/session/${sessionId}/webpage/${webpageId}/update`);
}

export const getWebpage = async (sessionId: string, webpageId: string): Promise<WebPage> => {
    return request.get<WebPage>(`/session/${sessionId}/webpage/${webpageId}`);
};
