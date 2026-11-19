package com.example.payments;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.util.Optional;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/** Checks the merchant's API key on /orders routes and sets the "merchantId" request attribute. */
@Configuration
public class AuthInterceptor implements HandlerInterceptor, WebMvcConfigurer {
    private final OrderStore store;

    public AuthInterceptor(OrderStore store) {
        this.store = store;
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(this).addPathPatterns("/orders/**");
    }

    @Override
    public boolean preHandle(HttpServletRequest req, HttpServletResponse res, Object handler)
            throws Exception {
        String key = Optional.ofNullable(req.getHeader("Authorization")).orElse("")
                .replaceFirst("^Bearer ", "");
        String merchantId = store.merchantForApiKey(key);
        if (merchantId == null) {
            res.sendError(HttpServletResponse.SC_UNAUTHORIZED);
            return false;
        }
        req.setAttribute("merchantId", merchantId);
        return true;
    }
}
