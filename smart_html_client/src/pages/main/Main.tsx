import React, { useEffect, useState, memo } from "react";

import { Session } from "../../request/model";

import { generateHtml, getSession } from "../../request/api"

import PromptInput from "../../components/PromptInput"
import HtmlIframe from "../../components/HtmlIframe"

const MemoHtml = memo(HtmlIframe)

import styles from './Main.module.scss';

const Main: React.FC = () => {
    const [loading, setLoading] = useState<boolean>(false)
    const [error, setError] = useState<boolean>(false)
    const [sessionReponse, setSessionReponse] = useState<Session>()

    const updateRequestHtml = async (prompt: string) => {
        try {
            const result = await generateHtml({ requirements: prompt })
            console.debug("updateRequestHtml => result: ", result);

            if (result.id) {
                localStorage.setItem('sessionId', result.id);
            }

            setSessionReponse(result)
            setLoading(false)
        } catch {
            setError(true)
        }
    }

    const sendPrompt = (prompt: string) => {
        console.debug("sendPrompt => prompt: ", prompt);
        setLoading(true)
        setError(false)
        void updateRequestHtml(prompt)
    }

    useEffect(() => {
        const fetchSessionData = async () => {
            const sessionId = localStorage.getItem('sessionId');
            if (sessionId) {
                setLoading(true);
                try {
                    const result = await getSession(sessionId);
                    setSessionReponse(result);
                    setLoading(false);
                } catch (error) {
                    setError(true)
                }
            }
        };

        fetchSessionData();
    }, []);

    return <div className={styles.main}>
        <MemoHtml
            loading={loading}
            webPage={sessionReponse?.web_pages[0]}
            error={error}
            delayLoading={true}
        />
        <div className={sessionReponse?.web_pages[0] ? `${styles['input-title-hidden']} ${styles['input-title']}` : styles['input-title']}>Let's create your dream web page</div>
        <PromptInput
            handleEnterDown={sendPrompt}
            loading={loading}
        />
    </div>
}

export default Main;
