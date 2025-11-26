'use client'

import React from 'react';
import { Provider as ReduxProvider } from 'react-redux';
import { store } from './store';

import { ApolloClient, InMemoryCache, ApolloProvider } from '@apollo/client';

// const client = new ApolloClient({
//     uri: "/graphql",       // 같은 Origin (Nginx) 기준 상대 경로
//     cache: new InMemoryCache(),
// });

const client = new ApolloClient({
    uri: "http://localhost:8000/graphql",
    cache: new InMemoryCache(),
});
const Providers = ({ children }: { children: React.ReactNode }) => {
    return (
        <ReduxProvider store={store}>
            <ApolloProvider client={client}>
                {children}
            </ApolloProvider>
        </ReduxProvider>
    );
};

export default Providers;
