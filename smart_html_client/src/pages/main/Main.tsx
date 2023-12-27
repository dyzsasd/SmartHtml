import React, { useEffect, useState, memo } from "react";

import { Session, WebPage } from "../../request/model";

import { generateHtml, getSession, comments, update, getWebpage} from "../../request/api"

import PromptInput from "../../components/PromptInput"
import HtmlIframe from "../../components/HtmlIframe"

const MemoHtml = memo(HtmlIframe)

import styles from './Main.module.scss';

const Main: React.FC = () => {
    const [loading, setLoading] = useState<boolean>(false)
    const [error, setError] = useState<boolean>(false)
    const [sessionReponse, setSessionReponse] = useState<Session>()

    const generateRequestHtml = async (prompt: string) => {
        try {
            const result = await generateHtml({ requirements: prompt })
            console.debug("generateRequestHtml => result: ", result);

            if (result._id) {
                localStorage.setItem('sessionId', result._id);
            }

            setSessionReponse(result)
            setLoading(false)
        } catch {
            setError(true)
        }
    }

    const updateRequestHtml = async (prompt: string) => { 
        try {
            if (sessionReponse){
                const lastPageId = sessionReponse.web_pages.at(-1)?._id;
                
                if (lastPageId){
                    const commentsResult = await comments(sessionReponse._id, lastPageId, prompt, {})
                    if (commentsResult){
                        const updateResult = await update(sessionReponse._id, lastPageId)
                        if (updateResult){
                            await intermittentTimerUpdate(sessionReponse._id, updateResult._id)
                        }
                    }
                }
            }
        } catch {
            setError(true)
        }
    }

    const intermittentTimerUpdate = async (sessionId: string, newWebpageId: string) => {
        const timer = setInterval(async () => {
            const result = await getWebpage(sessionId, newWebpageId)
            if (!result.in_processing){
                setLoading(false)
                clearInterval(timer)
                setSessionReponse(prevalue => {
                    if (prevalue){
                        prevalue.web_pages = [...prevalue.web_pages, result]
                        return prevalue
                    }
                })
            }
        }, 1000)
    }

    const sendPrompt = (prompt: string) => {
        console.debug("sendPrompt => prompt: ", prompt);
        setLoading(true)
        setError(false)
        if (!sessionReponse){
            void generateRequestHtml(prompt)
        }else{
            void updateRequestHtml(prompt)
        }
    }

    useEffect(() => {
        const fetchSessionData = async () => {
            const sessionId = localStorage.getItem('sessionId');
            if (sessionId) {
                setLoading(true);
                try {
                    const result = await getSession(sessionId);
                    setSessionReponse(result);
                    if (result.web_pages && result.web_pages.at(-1)?.in_processing){
                        intermittentTimerUpdate(sessionId, (result.web_pages.at(-1) as WebPage)._id)
                    }else{
                        setLoading(false);
                    }
                } catch (error) {
                    setError(true)
                }
            }
        };

        fetchSessionData();
    }, []);

    const reset = () => {
        localStorage.removeItem('sessionId')
        setSessionReponse(undefined)
        setError(false)
        setLoading(false)
    }

    return <div className={styles.main}>
        {sessionReponse &&
            <MemoHtml
                loading={loading}
                webPage={sessionReponse?.web_pages.at(-1)}
                error={error}
                delayLoading={true}
            />
        }
        <div className={sessionReponse?.web_pages.at(-1) ? `${styles['input-title-hidden']} ${styles['input-title']}` : styles['input-title']}>Let's create your dream web page</div>
        <PromptInput
            handleEnterDown={sendPrompt}
            reset={reset}
            loading={loading}
        />
    </div>
}

export default Main;
