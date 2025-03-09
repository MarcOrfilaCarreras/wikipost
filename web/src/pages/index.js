import React from "react";

import Main from "../layouts/main";
import Background from "../components/background";
import CTAButton from "../components/buttons/cta";
import Card from "../components/card";
import Window from "../components/window";
import EarthIcon from "../assets/icons/earth";
import PaperIcon from "../assets/icons/paper";
import SyncIcon from "../assets/icons/sync";
import PointerIcon from "../assets/icons/pointer";

const IndexPage = () => {
    return (
        <Main className="bg-gray-950 overflow-x-hidden">
            <Background />
            <main className="max-w-7xl w-full mx-auto relative z-10">
                <header className="pt-8 px-8 flex justify-between items-center">
                    <div className="flex items-center gap-4">
                        <img src="/img/icon.png" alt="Wikipost Logo" className="w-10 h-10" />
                        <h1 className="text-xl md:text-3xl font-extrabold text-gray-300">Wikipost</h1>
                    </div>
                    <nav className="flex flex-row items-center gap-6">
                        <a href="/auth/login" className="mx-4 hover:underline text-gray-300">
                            Login
                        </a>
                        <CTAButton text="Get started →" url="/auth/register" className={'hidden sm:block'}></CTAButton>
                    </nav>
                </header>

                <section className="flex flex-col pt-48 pb-32 px-8 text-center items-center gap-8">
                    <h2
                        className="text-3xl md:text-5xl font-extrabold leading-snug text-gray-300 flex flex-col"
                    >
                        <span>Share Wikipedia</span>
                        <span
                        >Knowledge on <span
                            className="text-transparent bg-clip-text bg-gradient-to-r from-purple-500 to-green-400"
                        >Instagram</span
                            >.</span
                        >
                    </h2>
                    <p className="text-md md:text-lg max-w-2xl text-center text-gray-300">
                        Effortlessly scrape, customize, and post Wikipedia articles to your Instagram feed with Wikipost. Turn knowledge into engaging content in seconds!
                    </p>
                    <CTAButton text="Get started →" url="/auth/register" className={'block sm:hidden'}></CTAButton>
                </section>

                <section className="py-16 px-8 text-center">
                    <h2 className="text-3xl md:text-4xl font-extrabold text-gray-300">Features</h2>
                    <p className="text-md md:text-lg text-gray-400 mt-4 max-w-2xl mx-auto">
                        Explore the powerful features that help you effortlessly scrape, customize, and post Wikipedia articles to Instagram.
                    </p>
                    <div className="mt-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        <Card title="Instant Wikipedia Scraping" subtitle="Easily scrape articles from Wikipedia and prepare them for sharing with just a few clicks.">
                            <EarthIcon></EarthIcon>
                        </Card>
                        <Card title="Customizable Posts" subtitle="Tailor the content and appearance of each post to suit your Instagram aesthetic before sharing.">
                            <PaperIcon></PaperIcon>
                        </Card>
                        <Card title="Seamless Integration" subtitle="Share your selected articles directly to Instagram without leaving the app—no extra steps needed.">
                            <SyncIcon></SyncIcon>
                        </Card>
                    </div>
                </section>

                <section className="relative overflow-hidden py-24">
                    <div className="container mx-auto px-4">
                        <div
                            className="flex flex-col-reverse lg:flex-row items-center justify-between gap-12"
                        >
                            <Window url="/img/showcase.jpg" />

                            <div className="max-w-xl">
                                <h2 className="text-3xl text-center lg:text-left md:text-4xl font-bold text-gray-300 mb-6">
                                    Sharing Wikipedia articles made simple
                                </h2>
                                <p className="text-gray-400 max-w-2xl mx-auto text-md md:text-lg mb-12">
                                    Take the effort out of sharing knowledge. Instantly scrape, customize, and post Wikipedia articles to your Instagram feed with ease.
                                </p>

                                <div className="space-y-8">
                                    <div className="flex items-start gap-4">
                                        <div
                                            className="flex-shrink-0 w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center"
                                        >
                                            <div className="w-6">
                                                <PointerIcon></PointerIcon>
                                            </div>
                                        </div>
                                        <div>
                                            <h3 className="text-white font-semibold text-lg mb-2">
                                                Effortless Article Scraping
                                            </h3>
                                            <p className="text-gray-400">
                                                Instantly scrape articles from Wikipedia with just a few clicks. No more searching and copying—your content is ready to share.
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <section className="py-16 px-8 text-center">
                    <div
                        className="bg-gradient-to-br from-gray-800/50 via-gray-800/30 to-gray-800/50 backdrop-blur-xl border border-gray-700/50 rounded-2xl p-8 md:p-12 shadow-xl"
                    >
                        <div className="relative mb-8">
                            <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-6">
                                <span
                                    className="bg-gradient-to-r from-purple-500 to-green-400 bg-clip-text text-transparent"
                                >
                                    Start sharing in minutes
                                </span>
                            </h2>

                            <p className="text-gray-400 text-lg mb-8 mx-auto">
                                Join thousands of users who are turning Wikipedia articles into engaging Instagram posts.
                                Sign up now and instantly start scraping, customizing, and sharing your favorite articles!
                            </p>
                        </div>

                        <div className="space-y-6">
                            <div
                                className="flex flex-col sm:flex-row items-center justify-center gap-4"
                            >
                                <CTAButton text="Get started →" url="/auth/register" />
                            </div>
                        </div>
                    </div>
                </section>

                <section className="flex flex-col pb-8 text-center items-center gap-8">
                    <footer>
                        <p className="text-xs md:text-sm text-gray-500">
                            © 2025 Wikipost. All rights reserved.
                        </p>
                    </footer>
                </section>
            </main>
        </Main>
    );
};

export default IndexPage;
