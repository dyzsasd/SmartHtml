import request from "./request";

import {
    GenerateHtmlRequest, Session
} from "./model"

export const generateHtml = async (requestModel: GenerateHtmlRequest): Promise<Session> => {
    return request.post<Session>('/session', requestModel);
};

export const getSession = async (sessionId: string): Promise<Session> => {
    return request.get<Session>(`/session/${sessionId}`);
};